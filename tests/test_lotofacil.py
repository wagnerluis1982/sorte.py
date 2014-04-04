# encoding=utf8

import basetest

from sortepy.loterica import Loteria

class LotofacilTest(basetest.BaseTestCase):
    def setUp(_):
        global lotofacil
        lotofacil = Loteria("lotofacil")

    def test_gerar_aposta(_):
        permitidos = set(range(1, 26))  # de 1 a 25

        # gerar lotofacil na quantidade padrão == 15
        aposta = lotofacil.gerar_aposta()
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), 15, "aposta não tem 15 números")
        _.eq(len(set(aposta)), 15, "aposta não tem 15 números diferentes")
        _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 25")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = lotofacil.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com mais de 15 números
        for n in range(16, 19):
            aposta = lotofacil.gerar_aposta(n)
            _.is_instance(aposta, tuple)
            _.eq(len(aposta), n, "aposta não tem %d números" % n)
            _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 25")
