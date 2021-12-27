# encoding=utf8

import errno
import http.cookiejar
import os
import re
import sqlite3
import time
import urllib.request

from typing import Any
from typing import Callable
from typing import MutableMapping
from typing import overload


def get_config_path(app: str = "sortepy") -> str:
    """Obtém o caminho de configuração de acordo com o SO

    Por enquanto é suportado os sistemas POSIX e Windows (NT)
    """
    # Linux, UNIX, BSD, ...
    if os.name == "posix":
        prefixo = ".config/"
        profile_dir = os.environ.get("HOME")

    # Windows 2000, XP, Vista, 7, 8, ...
    elif os.name == "nt":
        prefixo = ""
        profile_dir = os.environ.get("APPDATA")

    # Se nenhum SO suportado foi detectado, lança uma exceção
    else:
        raise NotImplementedError("Caminho de configuração não detectado")

    return os.path.join(profile_dir, prefixo + app)


def makedirs(caminho: str) -> None:
    """Versão própria do makedirs()

    Essa versão não lança exceção se o caminho já existir
    """
    try:
        os.makedirs(caminho)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Util:
    def __init__(self, cfg_path: str = None):
        # Se o caminho é uma string vazia, não deve ser usado nenhum cache
        # Definido para propósitos de teste
        if cfg_path == "":
            self.in_cache = False
            return

        # Se nenhum caminho foi passado, usa diretório de configuração padrão
        if cfg_path is None:
            try:
                cfg_path = get_config_path()
            # Pode ocorrer de não conseguir definir o diretório para cfg_path
            except NotImplementedError:
                self.in_cache = False
                return

        # Cria diretório de configuração, se não existir
        makedirs(cfg_path)

        # Define atributos de configuração
        self.__cfg_path = cfg_path
        self.pages_db = self.get_mapdb("paginas")
        self.in_cache = True

    def get_mapdb(self, name: str) -> "FileDB":
        db_path = os.path.join(self.__cfg_path, "%s.db" % name)
        return FileDB.open(db_path)

    def download(self, url: str, in_cache: bool = None) -> str:
        in_cache = in_cache if isinstance(in_cache, bool) else self.in_cache

        # Obtém a página do cache
        conteudo = None
        if in_cache:
            conteudo = self.cache(url)

        # Ou faz o download
        if conteudo is None:
            # As páginas de resultado de loterias exigem cookies
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            # A adição desse cookie dobra o tempo de resposta
            opener.addheaders.append(("Cookie", "security=true"))

            page = opener.open(url)
            content: bytes = page.read()

            charset = page.headers.get_param("charset")
            if charset is not None:
                conteudo = content.decode(charset)
            else:
                conteudo = content.decode()

            if in_cache:
                self.cache(url, conteudo)

        return conteudo

    @overload
    def cache(self, url: str) -> str:
        ...

    @overload
    def cache(self, url: str, conteudo: str) -> None:
        ...

    def cache(self, url, conteudo=None):
        # Sem conteúdo: leitura do cache
        if conteudo is None:
            if url not in self.pages_db:
                return None

            # obtém a entrada do cache
            result = self.pages_db[url]

            # se for uma entrada suja, verifica se já venceu o tempo para ficar nesse estado
            if self.is_dirty(result):
                timestamp, _ = result.split("|", 1)
                if time.time() > int(timestamp) + 1800:
                    del self.pages_db[url]
                return None
            else:
                return result

        # Do contrário: escrita no cache
        else:
            self.pages_db[url] = conteudo

    def blame(self, url: str) -> None:
        """Marca o resultado de uma URL como inválida.

        Isso é feito, registrando o horário em que esse método foi chamado.
        """
        if self.in_cache and url in self.pages_db:
            self.pages_db[url] = "%d|" % int(time.time())

    DIRTY_RE = re.compile(r"^[0-9]+\|")

    @classmethod
    def is_dirty(cls, s: str) -> re.Match:
        return cls.DIRTY_RE.match(s)


class FileDB(MutableMapping[str, str]):
    @staticmethod
    def open(filename: str) -> "FileDB":
        (prefix, _) = os.path.splitext(os.path.basename(filename))
        cls = _file_db_cls("sqlite")
        db = cls(filename, prefix)
        return db


def _file_db_cls(type: str) -> Callable[[str, str], FileDB]:
    class _SQLite3(FileDB):
        __version__ = 1

        def __init__(self, filename: str, prefix: str = "") -> None:
            self._con = sqlite3.connect(filename)
            self._table = prefix + "map"
            self._create_schema()

        def close(self) -> None:
            self._con.commit()
            self._con.close()

        def flush(self) -> None:
            self._con.commit()

        def __del__(self) -> None:
            try:
                self.close()
            except sqlite3.Error:
                pass

        def _create_schema(self) -> None:
            try:
                self._con.execute("BEGIN EXCLUSIVE TRANSACTION")
                self._con.execute(
                    "CREATE TABLE %s (key TEXT NOT NULL PRIMARY KEY, value TEXT NOT NULL, ttl INT)"
                    % self._table
                )
            # caso a tabela 'map' já exista, inicia-se o processo de migração
            except sqlite3.OperationalError:
                sql = self._migration_script()
                self._con.executescript(sql)
            finally:
                self._con.commit()
                self._write_dbversion(self.__version__)

        def _is_latest_version(self) -> bool:
            return self._read_dbversion() == self.__version__

        def _read_dbversion(self) -> int:
            (dbversion,) = self._con.execute("PRAGMA user_version").fetchone()
            return dbversion

        def _write_dbversion(self, version: int) -> None:
            self._con.execute("PRAGMA user_version = %d" % version)

        def _migration_script(self) -> str:
            # se versão for a mais atual, não é preciso criar esquema!
            dbversion = self._read_dbversion()
            if dbversion == self.__version__:
                return ""
            if dbversion == 0:
                sql_template = """
                    -- 1. Cria tabela temporária com o novo esquema
                    CREATE TABLE temp_{table} (key TEXT NOT NULL PRIMARY KEY, value TEXT NOT NULL, ttl INT);

                    -- 2. Copia dados da tabela atual para a temporária
                    INSERT INTO temp_{table}(key, value)
                    SELECT key, value FROM {table};

                    -- 3. Drop tabela atual
                    DROP TABLE {table};

                    -- 4. Renomeia tabela temporária
                    ALTER TABLE temp_{table}
                    RENAME TO {table};
                """
                return sql_template.format(table=self._table)
            return ""

        def get(self, key: str, default: str = None) -> str:  # type: ignore[override]
            try:
                return self[key]
            except KeyError:
                return default

        def __setitem__(self, key: str, value: str) -> None:
            with self._con as con:
                try:
                    con.execute(
                        "INSERT INTO %s(key, value) VALUES (?, ?)" % self._table,
                        (key, value),
                    )
                except sqlite3.IntegrityError:
                    con.execute(
                        "UPDATE %s SET value=? WHERE key=?" % self._table, (value, key)
                    )

        def __getitem__(self, key: str) -> str:
            cursor = self._con.cursor()
            cursor.execute("SELECT value FROM %s WHERE key=?" % self._table, (key,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise KeyError(key)

        def __delitem__(self, key: str) -> None:
            with self._con as con:
                con.execute("DELETE FROM %s WHERE key=?" % self._table, (key,))

        def __contains__(self, key: object) -> bool:
            cursor = self._con.cursor()
            cursor.execute("SELECT 1 FROM %s WHERE key=?" % self._table, (key,))
            return cursor.fetchall() != []

        def __enter__(self) -> FileDB:
            return self

        def __exit__(self, *args: Any) -> None:
            self.__del__()

        __iter__ = None
        __len__ = None

    if type == "sqlite":
        return _SQLite3

    raise
