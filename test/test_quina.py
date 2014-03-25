# encoding=utf8

from nose.tools import *

from gval.loteria import Loteria

class QuinaTest:
    def setup(self):
        global quina
        quina = Loteria("quina")

    def test_gerar_aposta(self):
        permitidos = set(range(1, 81))  # de 1 a 80

        aposta = quina.gerar_aposta()
        assert_is_instance(aposta, tuple)
        eq_(len(aposta), 5, "aposta não tem 5 números")
        eq_(len(set(aposta)), 5, "aposta não tem 5 números diferentes")
        ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 80")

        aposta2 = quina.gerar_aposta()
        assert_not_equal(aposta, aposta2, "segunda aposta igual à primeira")
