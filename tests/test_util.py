# encoding=utf8

import basetest

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import os
import threading

import sortepy.util


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
CONTEUDO_ENCODING = u"""<!DOCTYPE html>
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

class DownloadTest(basetest.BaseTestCase):
    'Util.download'

    @classmethod
    def setUpClass(cls):
        cls.server = FixtureHttpServer()
        cls.server.start()
        cls.base_url = "http://127.0.0.1:%d" % cls.server.port
        cls.util = sortepy.util.Util()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_download_pagina(_):
        url = _.base_url + '/pagina_ascii.html'
        _.eq(_.util.download(url), CONTEUDO_ASCII)

    def test_download_pagina_iso88591(_):
        url = _.base_url + '/pagina_iso-8859-1.html'
        conteudo = _.util.download(url)
        _.is_instance(conteudo, unicode)
        _.eq(conteudo, CONTEUDO_ENCODING % 'ISO-8859-1')

    def test_download_pagina_utf8(_):
        url = _.base_url + '/pagina_utf-8.html'
        conteudo = _.util.download(url)
        _.is_instance(conteudo, unicode)
        _.eq(conteudo, CONTEUDO_ENCODING % 'UTF-8')

    def test_download_pagina_charset_unknown(_):
        url = _.base_url + '/pagina_unknown.html'
        conteudo = _.util.download(url)
        _.is_instance(conteudo, str)


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
