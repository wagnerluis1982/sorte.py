import os
import sqlite3
import unittest

import sortepy.util
from basetest import tempdir

import fixtures
fixtures.start_server()

# Conteúdo para 'pagina_ascii.html'
CONTEUDO_ASCII = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="ASCII" />
        <title>Teste de sortepy.util</title>
    </head>
    <body>
        <h1>Teste</h1>
        <p>
            Fim do Teste
        </p>
    </body>
</html>
"""
# 'pagina_iso-8859-1.html' ou 'pagina_utf-8.html'
CONTEUDO_ENCODING = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="%s" />
        <title>Teste de sortepy.util</title>
    </head>
    <body>
        <h1>Teste cõm encódîngs</h1>
        <p>
            Fím do Testé
        </p>
    </body>
</html>
"""


class DownloadTest(unittest.TestCase):
    'Util.download'

    @classmethod
    def setUpClass(cls):
        cls.util = sortepy.util.Util(cfg_path='')

    def test_download_pagina(self):
        url = fixtures.server_url + '/paginas/pagina_ascii.html'
        assert self.util.download(url) == CONTEUDO_ASCII

    def test_download_pagina_iso88591(self):
        url = fixtures.server_url + '/paginas/pagina_iso-8859-1.html'
        conteudo = self.util.download(url)
        assert isinstance(conteudo, str)
        assert conteudo == CONTEUDO_ENCODING % 'ISO-8859-1'

    def test_download_pagina_utf8(self):
        url = fixtures.server_url + '/paginas/pagina_utf-8.html'
        conteudo = self.util.download(url)
        assert isinstance(conteudo, str)
        assert conteudo == CONTEUDO_ENCODING % 'UTF-8'

    def test_download_pagina_charset_unknown(self):
        url = fixtures.server_url + '/paginas/pagina_unknown.html'
        conteudo = self.util.download(url)
        assert isinstance(conteudo, str)


class CacheTest(unittest.TestCase):
    'Util.cache'

    def setUp(self):
        self.util = sortepy.util.Util(cfg_path=tempdir())

    def test_gravar_e_ler_cache(self):
        # gravação
        put_txt = 'Minha terra tem palmeiras, Onde canta o Sabiá'
        self.util.cache('dias.txt', put_txt)

        # leitura
        got_txt = self.util.cache('dias.txt')
        assert put_txt == got_txt

        # leitura falha
        assert self.util.cache('nao_existe') is None

    def test_guardar_e_recuperar_download(self):
        # baixa conteúdo e verifica se está em cache
        url = fixtures.server_url + '/paginas/pagina_ascii.html'
        self.util.download(url)
        assert self.util.cache(url) == CONTEUDO_ASCII

        # verifica se mesmo sem o servidor disponível o download ainda é feito
        # usando o cache
        assert self.util.download(url) == CONTEUDO_ASCII


class FileDBTest(unittest.TestCase):
    'FileDB'

    latest_version = 1

    def setUp(self):
        self.arquivo = os.path.join(tempdir(), 'test.db')

    def test_guardar_e_recuperar_valor(self):
        chave = 'cumprimento'
        valor = 'Olá, amigo, tudo bem?'
        db = self._open_db()
        db[chave] = valor
        db.close()

        # depois de fechar a base, tenta reabrir e ver se o valor continua lá
        db = self._open_db()
        assert db[chave] == valor
        db.close()

    def test_excluir_chave(self):
        chave = 'inutil'
        valor = 'Nada'
        db = self._open_db()
        db[chave] = valor
        assert chave in db, "chave '%s' não existe" % chave

        del db[chave]
        assert chave not in db, "chave '%s' não foi excluída" % chave
        db.close()

    def test_redefinir_valor(self):
        chave = 'chave'
        db = self._open_db()
        db[chave] = 'valor1'
        assert db[chave] == 'valor1'

        db[chave] = 'valor2'
        assert db[chave] == 'valor2'

    def test_upgrade_from_version_0(self):
        # cria tabela na v0
        table = 'testmap'

        key = 'tarzan'
        value = 'jane'

        conn = sqlite3.connect(self.arquivo)
        conn.execute('PRAGMA user_version = %d' % 0)
        conn.execute("CREATE TABLE %s (key TEXT PRIMARY KEY, value TEXT)" % table)
        conn.execute("INSERT INTO %s VALUES (?, ?)" % table, (key, value))
        conn.close()

        # depois de iniciar o FileDB
        db = self._open_db()
        db.close()

        # eu espero que o banco tenha sido convertido
        conn = sqlite3.connect(self.arquivo)
        (dbversion,) = conn.execute('PRAGMA user_version').fetchone()
        assert dbversion == self.latest_version

        # e a tabela tenha sido atualizada
        descriptions = self._table_descriptions(conn, table)
        assert descriptions['key'] == {'type': 'TEXT', 'notnull': True, 'dflt_value': None, 'pk': True}
        assert descriptions['value'] == {'type': 'TEXT', 'notnull': True, 'dflt_value': None, 'pk': False}
        assert descriptions['ttl'] == {'type': 'INT', 'notnull': False, 'dflt_value': None, 'pk': False}

    def _open_db(self):
        return sortepy.util.FileDB.open(self.arquivo)

    def _table_descriptions(self, conn, table):
        descriptions = conn.execute('PRAGMA table_info(%s)' % table).fetchall()
        return {
            row[1]: {
                'type': row[2],
                'notnull': row[3],
                'dflt_value': row[4],
                'pk': row[5],
            }
            for row in descriptions
        }
