import atexit
import shutil
import tempfile
import unittest

# patch para classe de loteria utilizar o servidor interno
import patchs

from sortepy.loterica import Loteria


patchs.loteria_class()


def tempdir(custom_prefix="sortepy-"):
    newdir = tempfile.mkdtemp(prefix=custom_prefix)
    atexit.register(shutil.rmtree, newdir)
    return newdir


# preparando paths do projeto para os testes
cfg_fixture_path = tempdir()


class LoteriaTestCase(unittest.TestCase):
    nome = ""
    # set com a faixa completa de números que podem ser apostados
    permitidos = frozenset()
    # tuple com a quantidade de números para gerar as apostas, primeiro
    # elemento é a aposta na quantidade padrão
    numeros = ()

    # número do concurso para consultar
    concurso = 0
    # resultados da consulta para o concurso especificado
    sorteios = ()

    # apostas para conferir
    apostas = ()
    # resultados esperados das conferências
    esperados = None

    def __init__(self, *args, **kwargs):
        if self.permitidos:
            self.infsup = min(self.permitidos), max(self.permitidos)
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.loto = Loteria(self.nome, cfg_path=cfg_fixture_path)

    def test_gerar_aposta(self):
        # gerar aposta na quantidade padrão
        aposta = self.check_gerar_aposta(None)

        # outra aposta para identificar se realmente é aleatório
        aposta2 = self.loto.gerar_aposta()
        assert aposta != aposta2, "segunda aposta igual à primeira"

        # apostas com outras quantidades de números
        for n in self.numeros[1:]:
            self.check_gerar_aposta(n)

    def test_consultar_resultado(self):
        result = self.loto.consultar(self.concurso)
        assert isinstance(result, dict)
        assert result["concurso"] == self.concurso
        assert result["numeros"] == self.sorteios

    def test_conferir_aposta(self):
        resp = self.loto.conferir(self.concurso, self.apostas[:1])
        assert isinstance(resp, list)
        assert resp[0]["concurso"] == self.concurso
        assert resp[0]["numeros"] == self.apostas[0]
        assert resp[0]["acertou"] == self.esperados["acertou"][0]
        assert resp[0]["ganhou"] == self.esperados["ganhou"][0]

    def test_conferir_varias_apostas(self):
        resp = self.loto.conferir(self.concurso, self.apostas)
        assert isinstance(resp, list)
        for i in range(len(self.apostas)):
            assert resp[i]["concurso"] == self.concurso
            assert resp[i]["numeros"] == self.apostas[i]
            assert resp[i]["acertou"] == self.esperados["acertou"][i]
            assert resp[i]["ganhou"] == self.esperados["ganhou"][i]

    def check_gerar_aposta(self, n):
        n = n or self.numeros[0]  # número padrão ou informado

        aposta = self.loto.gerar_aposta(n)
        assert isinstance(aposta, tuple)
        assert len(aposta) == n, "aposta não tem %d números" % n
        assert len(set(aposta)) == n, "aposta não tem %d números diferentes" % n
        assert self.permitidos.issuperset(aposta), (
            "aposta não está entre %d e %d" % self.infsup
        )

        return aposta
