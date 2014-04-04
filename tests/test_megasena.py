# encoding=utf8

import basetest

from gval.loterica import Loteria

class MegaSenaTest(basetest.BaseTestCase):
    'Mega-Sena'

    def setUp(_):
        global sena
        sena = Loteria("megasena")

    def test_gerar_aposta(_):
        permitidos = set(range(1, 61))  # de 1 a 60

        # gerar sena na quantidade padrão == 6
        aposta = sena.gerar_aposta()
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), 6, "aposta não tem 6 números")
        _.eq(len(set(aposta)), 6, "aposta não tem 6 números diferentes")
        _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 60")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = sena.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com mais de 6 números
        for n in range(7, 16):
            aposta = sena.gerar_aposta(n)
            _.is_instance(aposta, tuple)
            _.eq(len(aposta), n, "aposta não tem %d números" % n)
            _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 60")
