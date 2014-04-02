# encoding=utf8

from nose.tools import *

from gval.loteria import Loteria

class MegaSenaTest:
    'Mega-Sena'

    def setup(self):
        global sena
        sena = Loteria("megasena")

    def test_gerar_aposta(self):
        permitidos = set(range(1, 61))  # de 1 a 60

        # gerar sena na quantidade padrão == 6
        aposta = sena.gerar_aposta()
        assert_is_instance(aposta, tuple)
        eq_(len(aposta), 6, "aposta não tem 6 números")
        eq_(len(set(aposta)), 6, "aposta não tem 6 números diferentes")
        ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 60")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = sena.gerar_aposta()
        assert_not_equal(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com mais de 6 números
        for n in range(7, 16):
            aposta = sena.gerar_aposta(n)
            assert_is_instance(aposta, tuple)
            eq_(len(aposta), n, "aposta não tem %d números" % n)
            eq_(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            ok_(permitidos.issuperset(aposta), "aposta não está entre 1 e 60")
