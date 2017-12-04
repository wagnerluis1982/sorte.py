import os
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
