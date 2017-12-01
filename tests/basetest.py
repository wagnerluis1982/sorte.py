# encoding=utf8

import atexit
import os
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

    def test_gerar_aposta(_):
        # gerar aposta na quantidade padrão
        aposta = _.check_gerar_aposta(None)

        # outra aposta para identificar se realmente é aleatório
        aposta2 = _.loto.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com outras quantidades de números
        for n in _.numeros[1:]:
            _.check_gerar_aposta(n)

    def test_consultar_resultado(_):
        result = _.loto.consultar(_.concurso)
        _.is_instance(result, dict)
        _.eq(result['concurso'], _.concurso)
        _.eq(result['numeros'], _.sorteios)

    def test_conferir_aposta(_):
        resp = _.loto.conferir(_.concurso, _.apostas[:1])
        _.is_instance(resp, list)
        _.eq(resp[0]['concurso'], _.concurso)
        _.eq(resp[0]['numeros'], _.apostas[0])
        _.eq(resp[0]['acertou'], _.esperados['acertou'][0])
        _.eq(resp[0]['ganhou'], _.esperados['ganhou'][0])

    def test_conferir_varias_apostas(_):
        resp = _.loto.conferir(_.concurso, _.apostas)
        _.is_instance(resp, list)
        for i in range(len(_.apostas)):
            _.eq(resp[i]['concurso'], _.concurso)
            _.eq(resp[i]['numeros'], _.apostas[i])
            _.eq(resp[i]['acertou'], _.esperados['acertou'][i])
            _.eq(resp[i]['ganhou'], _.esperados['ganhou'][i])

    def check_gerar_aposta(_, n):
        n = n or _.numeros[0]  # número padrão ou informado

        aposta = _.loto.gerar_aposta(n)
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), n, "aposta não tem %d números" % n)
        _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
        _.ok(_.permitidos.issuperset(aposta),
             "aposta não está entre %d e %d" % _.infsup)

        return aposta
