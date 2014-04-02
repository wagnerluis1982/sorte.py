# encoding=utf8

from nose.tools import *

from gval.loteria import Loteria

class LotomaniaTest:
    def setup(self):
        global lotomania
        lotomania = Loteria("lotomania")

    def test_gerar_aposta(self):
        permitidos = set(range(1, 101))  # de 1 a 100

        # gerar lotomania na quantidade padrão == 50
        aposta = lotomania.gerar_aposta()
        assert_is_instance(aposta, tuple)
        eq_(len(aposta), 50, "aposta não tem 50 números")
        eq_(len(set(aposta)), 50, "aposta não tem 50 números diferentes")
        ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 100")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = lotomania.gerar_aposta()
        assert_not_equal(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com outras quantidade de números
        for n in (5, 7, 10, 15, 20, 30, 40, 45):
            aposta = lotomania.gerar_aposta(n)
            assert_is_instance(aposta, tuple)
            eq_(len(aposta), n, "aposta não tem %d números" % n)
            eq_(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 100")
