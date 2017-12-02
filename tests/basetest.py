# encoding=utf8

import atexit
import shutil
import tempfile
from unittest import TestCase

from sortepy.loterica import Loteria


def tempdir(custom_prefix='sortepy-'):
    newdir = tempfile.mkdtemp(prefix=custom_prefix)
    atexit.register(shutil.rmtree, newdir)
    return newdir


# preparando paths do projeto para os testes
cfg_fixture_path = tempdir()


class BaseTestCase(TestCase):
    longMessage = True

    # asserts com nomes mais legais
    is_instance = TestCase.assertIsInstance
    is_none = TestCase.assertIsNone
    eq = TestCase.assertEqual
    not_eq = TestCase.assertNotEqual
    ok = TestCase.assertTrue


class LoteriaTestCase(BaseTestCase):
    nome = ""
    # set com a faixa completa de números que podem ser apostados
    permitidos = frozenset()
    # tuple com a quantidade de números para gerar as apostas, primeiro
    # elemento é a aposta na quantidade padrão
    numeros = ()

    # número do concurso para consultar
    concurso = 0
    # resultados da consulta para o concurso especificado
    sorteios = ()

    # apostas para conferir
    apostas = ()
    # resultados esperados das conferências
    esperados = None

    def __init__(self, *args, **kwargs):
        if self.permitidos:
            self.infsup = min(self.permitidos), max(self.permitidos)
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.loto = Loteria(self.nome, cfg_path=cfg_fixture_path)

    def test_gerar_aposta(self):
        # gerar aposta na quantidade padrão
        aposta = self.check_gerar_aposta(None)

        # outra aposta para identificar se realmente é aleatório
        aposta2 = self.loto.gerar_aposta()
        self.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com outras quantidades de números
        for n in self.numeros[1:]:
            self.check_gerar_aposta(n)

    def test_consultar_resultado(self):
        result = self.loto.consultar(self.concurso)
        self.is_instance(result, dict)
        self.eq(result['concurso'], self.concurso)
        self.eq(result['numeros'], self.sorteios)

    def test_conferir_aposta(self):
        resp = self.loto.conferir(self.concurso, self.apostas[:1])
        self.is_instance(resp, list)
        self.eq(resp[0]['concurso'], self.concurso)
        self.eq(resp[0]['numeros'], self.apostas[0])
        self.eq(resp[0]['acertou'], self.esperados['acertou'][0])
        self.eq(resp[0]['ganhou'], self.esperados['ganhou'][0])

    def test_conferir_varias_apostas(self):
        resp = self.loto.conferir(self.concurso, self.apostas)
        self.is_instance(resp, list)
        for i in range(len(self.apostas)):
            self.eq(resp[i]['concurso'], self.concurso)
            self.eq(resp[i]['numeros'], self.apostas[i])
            self.eq(resp[i]['acertou'], self.esperados['acertou'][i])
            self.eq(resp[i]['ganhou'], self.esperados['ganhou'][i])

    def check_gerar_aposta(self, n):
        n = n or self.numeros[0]  # número padrão ou informado

        aposta = self.loto.gerar_aposta(n)
        self.is_instance(aposta, tuple)
        self.eq(len(aposta), n, "aposta não tem %d números" % n)
        self.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
        self.ok(self.permitidos.issuperset(aposta),
             "aposta não está entre %d e %d" % self.infsup)

        return aposta
