# encoding=utf8

import http.cookiejar
import errno
import os
import re
import sqlite3
import urllib.request
import time


def get_config_path(app='sortepy'):
    """Obtém o caminho de configuração de acordo com o SO

    Por enquanto é suportado os sistemas POSIX e Windows (NT)
    """
    # Linux, UNIX, BSD, ...
    if os.name == 'posix':
        prefixo = '.config/'
        profile_dir = os.environ.get("HOME")

    # Windows 2000, XP, Vista, 7, 8, ...
    elif os.name == 'nt':
        prefixo = ''
        profile_dir = os.environ.get("APPDATA")

    # Se nenhum SO suportado foi detectado, lança uma exceção
    else:
        raise NotImplementedError("Caminho de configuração não detectado")

    return os.path.join(profile_dir, prefixo + app)


def makedirs(caminho):
    """Versão própria do makedirs()

    Essa versão não lança exceção se o caminho já existir
    """
    try:
        os.makedirs(caminho)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Util:
    def __init__(self, cfg_path=None):
        # Se o caminho é uma string vazia, não deve ser usado nenhum cache
        # Definido para propósitos de teste
        if cfg_path == '':
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

        # Cria diretórios de configuração, se não existirem
        self.cache_path = os.path.join(cfg_path, 'cache')
        makedirs(self.cache_path)

        # Define atributos de configuração
        self.pages_db = self.get_db('paginas')
        self.in_cache = True

    def get_db(self, name):
        return FileDB.open(os.path.join(self.cache_path, name + '.db'))

    def download(self, url, in_cache=None):
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
            conteudo = page.read()

            charset = page.headers.get_param('charset')
            if charset is not None:
                conteudo = conteudo.decode(charset)
            else:
                conteudo = conteudo.decode()

            if in_cache:
                self.cache(url, conteudo)

        return conteudo

    def cache(self, url, conteudo=None):
        # Sem conteúdo: leitura do cache
        if conteudo is None:
            if url not in self.pages_db:
                return None

            # obtém a entrada do cache
            result = self.pages_db[url]

            # se for uma entrada suja, verifica se já venceu o tempo para ficar nesse estado
            if self.is_dirty(result):
                timestamp, _ = result.split('|', 1)
                if time.time() > int(timestamp) + 1800:
                    del self.pages_db[url]
                return None
            else:
                return result

        # Do contrário: escrita no cache
        else:
            self.pages_db[url] = conteudo

    def blame(self, url):
        """Marca o resultado de uma URL como inválida.

        Isso é feito, registrando o horário em que esse método foi chamado.
        """
        if self.in_cache and url in self.pages_db:
            self.pages_db[url] = "%d|" % int(time.time())

    DIRTY_RE = re.compile(r'^[0-9]+\|')

    @classmethod
    def is_dirty(cls, s):
        return cls.DIRTY_RE.match(s)


class FileDB:
    @staticmethod
    def open(filename):
        db = FileDB._SQLite3(filename)
        return db

    class _SQLite3(object):
        __version__ = 0  # por enquanto não serve para nada

        def __init__(self, filename):
            self._con = sqlite3.connect(filename)
            self._create_schema()

        def close(self):
            self._con.commit()
            self._con.close()

        def flush(self):
            self._con.commit()

        def __del__(self):
            try:
                self.close()
            except sqlite3.Error:
                pass

        def _create_schema(self):
            try:
                self._con.execute("CREATE TABLE map (key TEXT PRIMARY KEY, value TEXT)")
                self._write_dbversion(self.__version__)
            # caso a tabela 'map' já exista
            except sqlite3.OperationalError:
                pass

        def _read_dbversion(self):
            (dbversion,) = self._con.execute('PRAGMA user_version').fetchone()
            return dbversion

        def _write_dbversion(self, version):
            self._con.execute('PRAGMA user_version = %d' % version)

        def get(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                return default

        def __setitem__(self, key, value):
            with self._con as con:
                try:
                    con.execute("INSERT INTO map VALUES (?, ?)", (key, value))
                except sqlite3.IntegrityError:
                    con.execute("UPDATE map SET value=? WHERE key=?", (value, key))

        def __getitem__(self, key):
            cursor = self._con.cursor()
            cursor.execute("SELECT value FROM map WHERE key=?", (key,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise KeyError(key)

        def __delitem__(self, key):
            with self._con as con:
                con.execute("DELETE FROM map WHERE key=?", (key,))

        def __contains__(self, key):
            cursor = self._con.cursor()
            cursor.execute("SELECT 1 FROM map WHERE key=?", (key,))
            return cursor.fetchall() != []

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.__del__()
