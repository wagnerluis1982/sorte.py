import pytest

import basetest


pytestmark = pytest.mark.v1


class FederalTest(basetest.LoteriaTestCase):
    "Loteria Federal"

    # atributos do teste de consulta
    nome = "federal"
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
    esperados = {
        "acertou": ([[37715]], [[24797]], []),
        "ganhou": (["700.000,00"], ["24.700,00"], ["0,00"]),
    }

    # teste com as regras específicas da federal
    def test_consultar_resultado(self):
        result = self.loto.consultar(self.concurso)
        assert isinstance(result, dict)
        assert result["concurso"] == self.concurso
        assert result["premios"] == self.premios

    # testes da superclasse removidos
    test_gerar_aposta = None
