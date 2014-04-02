# encoding=utf8

from nose.tools import *

from gval.loteria import Loteria

class LotofacilTest:
    def setup(self):
        global lotofacil
        lotofacil = Loteria("lotofacil")

    def test_gerar_aposta(self):
        permitidos = set(range(1, 26))  # de 1 a 25

        # gerar lotofacil na quantidade padrão == 15
        aposta = lotofacil.gerar_aposta()
        assert_is_instance(aposta, tuple)
        eq_(len(aposta), 15, "aposta não tem 15 números")
        eq_(len(set(aposta)), 15, "aposta não tem 15 números diferentes")
        ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 25")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = lotofacil.gerar_aposta()
        assert_not_equal(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com mais de 15 números
        for n in range(16, 21):
            aposta = lotofacil.gerar_aposta(n)
            assert_is_instance(aposta, tuple)
            eq_(len(aposta), n, "aposta não tem %d números" % n)
            eq_(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 25")
