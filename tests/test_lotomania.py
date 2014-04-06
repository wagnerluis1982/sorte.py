# encoding=utf8

import basetest

from sortepy.loterica import Loteria

class LotomaniaTest(basetest.BaseTestCase):
    def setUp(_):
        global lotomania
        lotomania = Loteria("lotomania")

    def test_gerar_aposta(_):
        permitidos = set(range(1, 101))  # de 1 a 100

        # gerar lotomania na quantidade padrão == 20
        aposta = lotomania.gerar_aposta()
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), 20, "aposta não tem 20 números")
        _.eq(len(set(aposta)), 20, "aposta não tem 20 números diferentes")
        _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 100")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = lotomania.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com outras quantidade de números
        for n in (5, 7, 10, 15, 20, 30, 40, 45):
            aposta = lotomania.gerar_aposta(n)
            _.is_instance(aposta, tuple)
            _.eq(len(aposta), n, "aposta não tem %d números" % n)
            _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 100")
