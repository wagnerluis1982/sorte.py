# encoding=utf8

import os
import threading
import unittest
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

import sortepy.util
from basetest import tempdir

# Diretório de páginas: '/tests/fixtures/paginas'
PAGES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures', 'paginas')
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
        cls.server = FixtureHttpServer()
        cls.server.start()
        cls.base_url = "http://127.0.0.1:%d" % cls.server.port
        cls.util = sortepy.util.Util(cfg_path='')

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_download_pagina(self):
        url = self.base_url + '/pagina_ascii.html'
        assert self.util.download(url) == CONTEUDO_ASCII

    def test_download_pagina_iso88591(self):
        url = self.base_url + '/pagina_iso-8859-1.html'
        conteudo = self.util.download(url)
        assert isinstance(conteudo, str)
        assert conteudo == CONTEUDO_ENCODING % 'ISO-8859-1'

    def test_download_pagina_utf8(self):
        url = self.base_url + '/pagina_utf-8.html'
        conteudo = self.util.download(url)
        assert isinstance(conteudo, str)
        assert conteudo == CONTEUDO_ENCODING % 'UTF-8'

    def test_download_pagina_charset_unknown(self):
        url = self.base_url + '/pagina_unknown.html'
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
        server = FixtureHttpServer()
        server.start()
        base_url = "http://127.0.0.1:%d" % server.port

        # baixa conteúdo e verifica se está em cache
        url = base_url + '/pagina_ascii.html'
        try:
            self.util.download(url)
            assert self.util.cache(url) == CONTEUDO_ASCII
        finally:
            server.stop()

        # verifica se mesmo sem o servidor disponível o download ainda é feito
        # usando o cache
        assert self.util.download(url) == CONTEUDO_ASCII


class FileDBTest(unittest.TestCase):
    'FileDB'

    def setUp(self):
        self.arquivo = os.path.join(tempdir(), 'test.db')
        self.db = sortepy.util.FileDB.open(self.arquivo)

    def test_guardar_e_recuperar_valor(self):
        chave = 'cumprimento'
        valor = 'Olá, amigo, tudo bem?'
        self.db[chave] = valor
        self.db.close()

        # depois de fechar a base, tenta reabrir e ver se o valor continua lá
        db = sortepy.util.FileDB.open(self.arquivo)
        assert db[chave] == valor
        db.close()

    def test_excluir_chave(self):
        chave = 'inutil'
        valor = 'Nada'
        self.db[chave] = valor
        assert chave in self.db, "chave '%s' não existe" % chave

        del self.db[chave]
        assert chave not in self.db, "chave '%s' não foi excluída" % chave
        self.db.close()

    def test_redefinir_valor(self):
        chave = 'chave'
        self.db[chave] = 'valor1'
        assert self.db[chave] == 'valor1'

        self.db[chave] = 'valor2'
        assert self.db[chave] == 'valor2'


class FixtureRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        # Desabilitando mensagens de log no terminal.
        pass

    def guess_type(self, path):
        # Se nome do arquivo indica um charset retorna 'text/html' e charset
        for charset in ('ascii', 'iso-8859-1', 'utf-8'):
            if charset in path:
                return "text/html; charset=%s" % charset
        # Se não achou um charset retorna mimetype default
        return SimpleHTTPRequestHandler.guess_type(self, path)


class FixtureHttpServer(object):
    def __init__(self):
        os.chdir(PAGES_DIR)
        httpd = HTTPServer(('127.0.0.1', 0), FixtureRequestHandler)
        self.thread = threading.Thread(target=httpd.serve_forever)
        self.httpd = httpd
        self.port = httpd.server_port

    def start(self):
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
