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

    def test_consultar_resultado(self):
        result = self.loto.consultar(self.concurso)
        assert isinstance(result, dict)
        assert result['concurso'] == self.concurso
        assert result['premios'] == self.premios
