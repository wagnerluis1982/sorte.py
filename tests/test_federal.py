import unittest
import basetest
from sortepy.loterica import Loteria


class FederalTest(unittest.TestCase):
    'Loteria Federal'

    def setUp(self):
        self.loto = Loteria("federal", cfg_path=basetest.cfg_fixture_path)

    # atributos do teste de consulta
    concurso = 5235
    premios = {
        37715: "700.000,00",
        69587: "36.000,00",
        10591: "30.000,00",
        24797: "24.700,00",
        29693: "20.146,00",
    }

    # atributos dos testes de conferência de bilhetes
    apostas = [[37715], [24797], [12345]]
    esperados = {'acertou': ([[37715]], [[24797]], []),
                 'ganhou': (['700.000,00'], ['24.700,00'], ['0,00'])}

    def test_consultar_resultado(self):
        result = self.loto.consultar(self.concurso)
        assert isinstance(result, dict)
        assert result['concurso'] == self.concurso
        assert result['premios'] == self.premios

    def test_conferir_aposta(self):
        resp = self.loto.conferir(self.concurso, self.apostas[:1])
        assert isinstance(resp, list)
        assert resp[0]['concurso'] == self.concurso
        assert resp[0]['numeros'] == self.apostas[0]
        assert resp[0]['acertou'] == self.esperados['acertou'][0]
        assert resp[0]['ganhou'] == self.esperados['ganhou'][0]

    def test_conferir_varias_apostas(self):
        resp = self.loto.conferir(self.concurso, self.apostas)
        assert isinstance(resp, list)
        for i in range(len(self.apostas)):
            assert resp[i]['concurso'] == self.concurso
            assert resp[i]['numeros'] == self.apostas[i]
            assert resp[i]['acertou'] == self.esperados['acertou'][i]
            assert resp[i]['ganhou'] == self.esperados['ganhou'][i]
