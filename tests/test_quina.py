# encoding=utf8

import basetest

from sortepy.loterica import Loteria

class QuinaTest(basetest.BaseTestCase):
    def setUp(self):
        self.quina = Loteria("quina")

    def test_gerar_aposta(_):
        permitidos = set(range(1, 81))  # de 1 a 80

        # gerar quina na quantidade padrão == 5
        aposta = _.quina.gerar_aposta()
        _.is_instance(aposta, tuple)
        _.eq(len(aposta), 5, "aposta não tem 5 números")
        _.eq(len(set(aposta)), 5, "aposta não tem 5 números diferentes")
        _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 80")

        # outra aposta para identificar se realmente é aleatório
        aposta2 = _.quina.gerar_aposta()
        _.not_eq(aposta, aposta2, "segunda aposta igual à primeira")

        # apostas com mais de 5 números
        for n in (6, 7):
            aposta = _.quina.gerar_aposta(n)
            _.is_instance(aposta, tuple)
            _.eq(len(aposta), n, "aposta não tem %d números" % n)
            _.eq(len(set(aposta)), n, "aposta não tem %d números diferentes" % n)
            _.ok(permitidos.issuperset(aposta), "aposta não está entre 1 e 80")
