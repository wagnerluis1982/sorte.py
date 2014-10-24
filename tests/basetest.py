# encoding=utf8

import sys
import os

from unittest import TestCase

# preparando path do projeto para os testes
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sortepy.loterica import Loteria


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
    permitidos = ()
    # tuple com a quantidade de números para gerar as apostas, primeiro
    # elemento é a aposta na quantidade padrão
    numeros = ()

    def __init__(self, *args, **kwargs):
        if self.permitidos:
            self.infsup = min(self.permitidos), max(self.permitidos)
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.loto = Loteria(self.nome)

    def test_gerar_aposta(_):
        # gerar aposta na quantidade padrão
        aposta = _.check_gerar_aposta(None)

        # outra aposta para identificar se realmente é aleatório
        aposta2 = _.loto.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com outras quantidades de números
        for n in _.numeros[1:]:
            _.check_gerar_aposta(n)

    def check_gerar_aposta(_, n):
        n = n or _.numeros[0]  # número padrão ou informado

        aposta = _.loto.gerar_aposta(n)
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), n, "aposta não tem %d números" % n)
        _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
        _.ok(_.permitidos.issuperset(aposta),
             "aposta não está entre %d e %d" % _.infsup)

        return aposta
