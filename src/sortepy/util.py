# encoding=utf8

import codecs
import cookielib
import errno
import os
import re
import sqlite3
import urllib2


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


class Util(object):
    def __init__(self, cfg_path=None):
        # Se nenhum caminho foi passado, usa diretório de configuração padrão
        if cfg_path is None:
            try:
                cfg_path = get_config_path()
            except NotImplementedError:
                self.usar_cache = False
                return
            else:
                self.cfg_path = cfg_path
                self.pages_cache = os.path.join(cfg_path, 'cache', 'paginas')
                self.usar_cache = True

        # Se o caminho é False, indica que não deve ser usado nenhum cache
        # Definido para propósitos de teste
        elif cfg_path is False:
            self.usar_cache = False
            return

        # Caso contrário, usa o caminho passado pelo argumento
        else:
            self.cfg_path = cfg_path
            self.pages_cache = os.path.join(cfg_path, 'cache', 'paginas')
            self.usar_cache = True

        # Cria diretórios de cache, caso necessário
        if self.usar_cache:
            makedirs(self.pages_cache)

    def download(self, url, usar_cache=False):
        usar_cache = usar_cache or self.usar_cache

        # Obtém a página do cache
        conteudo = None
        if usar_cache:
            conteudo = self.cache(url)

        # Ou faz o download
        if conteudo is None:
            # As páginas de resultado de loterias exigem cookies
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            # A adição desse cookie dobra o tempo de resposta
            opener.addheaders.append(("Cookie", "security=true"))

            page = opener.open(url)
            conteudo = page.read()

            charset = page.headers.getparam('charset')
            if charset is not None:
                try:
                    conteudo = unicode(conteudo, charset)
                except (UnicodeDecodeError, LookupError):
                    pass

            if usar_cache:
                self.cache(url, conteudo)

        return conteudo

    def cache(self, url, conteudo=None):
        # Caminho com nome seguro
        caminho = os.path.join(self.pages_cache, re.sub('[:/?]', '_', url))

        # Sem contéudo: leitura do cache
        if conteudo is None:
            try:
                f = codecs.open(caminho, 'r', encoding='utf-8')
            except IOError:
                return None
            else:
                conteudo = f.read()
                f.close()
                return conteudo

        # Do contrário: escrita no cache
        else:
            f = codecs.open(caminho, 'w', encoding='utf-8')
            f.write(conteudo)
            f.close()


class FileDB:
    @staticmethod
    def open(filename):
        db = FileDB._SQLite3(filename)
        return db

    class _SQLite3(object):
        __version__ = 0  # por enquanto não serve para nada

        def __init__(self, filename):
            self._conn = sqlite3.connect(filename)
            self._cur = self._conn.cursor()
            self._create_schema()

        def close(self):
            self._conn.commit()
            self._conn.close()

        def __del__(self):
            try:
                self.close()
            except sqlite3.ProgrammingError:
                pass

        def _create_schema(self):
            cursor = self._cur
            try:
                cursor.execute("CREATE TABLE map (key PRIMARY KEY, value)")
                self._write_dbversion(self.__version__)
            # caso a tabela 'map' já exista
            except sqlite3.OperationalError:
                pass

        def _read_dbversion(self):
            cursor = self._cur
            (dbversion,) = cursor.execute('PRAGMA user_version').fetchone()
            return dbversion

        def _write_dbversion(self, version):
            cursor = self._cur
            cursor.execute('PRAGMA user_version = %d' % version)

        def __setitem__(self, key, value):
            cursor = self._cur
            try:
                cursor.execute("INSERT INTO map VALUES (?, ?)", (key, value))
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE map SET value=? WHERE key=?",
                               (value, key))

        def __getitem__(self, key):
            cursor = self._cur
            cursor.execute("SELECT value FROM map WHERE key=?", (key,))
            (value,) = cursor.fetchone()
            return value

        def __delitem__(self, key):
            cursor = self._cur
            cursor.execute("DELETE FROM map WHERE key=?", (key,))

        def __contains__(self, key):
            cursor = self._cur
            cursor.execute("SELECT 1 FROM map WHERE key=?", (key,))
            return cursor.fetchall() != []
