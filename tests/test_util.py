# encoding=utf8

import basetest

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import atexit
import os
import shutil
import tempfile
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
        cls.util = sortepy.util.Util(cfg_path=False)

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


class CacheTest(basetest.BaseTestCase):
    'Util.cache'

    def setUp(self):
        self.util = sortepy.util.Util(cfg_path=tempdir())
        self.cache = self.util.pages_cache

    def test_gravar_e_ler_cache(_):
        # gravação
        put_txt = u'Minha terra tem palmeiras, Onde canta o Sabiá'
        _.util.cache('dias.txt', put_txt)
        _.ok(os.path.exists(os.path.join(_.cache, 'dias.txt')))

        # leitura
        got_txt = _.util.cache('dias.txt')
        _.eq(put_txt, got_txt)

        # leitura falha
        _.is_none(_.util.cache('nao_existe'))

    def test_guardar_e_recuperar_download(_):
        server = FixtureHttpServer()
        server.start()
        base_url = "http://127.0.0.1:%d" % server.port

        # baixa conteúdo e verifica se arquivo foi criado
        filename = 'http___127.0.0.1_%d_pagina_ascii.html' % server.port
        try:
            _.util.download(base_url + '/pagina_ascii.html')
            _.ok(os.path.exists(os.path.join(_.cache, filename)))
        finally:
            server.stop()

        # verifica se mesmo sem o servidor disponível o cache ainda é
        # encontrado
        url = base_url + '/pagina_ascii.html'
        _.eq(_.util.download(url), CONTEUDO_ASCII)


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


def tempdir(custom_prefix='sortepy-'):
    newdir = tempfile.mkdtemp(prefix=custom_prefix)
    atexit.register(shutil.rmtree, newdir)
    return newdir
