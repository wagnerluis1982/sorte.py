import io
import unittest

import basetest
import sortepy.script

def run_script(args):
    output = io.StringIO()
    sortepy.script.main(args, stdout=output, cfg_path=basetest.cfg_fixture_path)
    output.seek(0)
    return output.readlines()


# Os testes do script são focados na loteria da Quina porque tem menos números
# para verificar. Caso necessário, testes com outras loterias serão criados.
# Como todas as loterias possuem testes individuais, isto não é um grande
# problema.
class ScriptTest(unittest.TestCase):
    def test_gerar_UMA_aposta_padrao(self):
        # geração de aposta da quina padrão com 5 números
        args = (None, 'quina')
        readlines = run_script(args)
        linha = readlines[1]
        assert len([int(x) for x in linha.split()]) == 5

    def test_gerar_UMA_aposta_nao_padrao(self):
        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
            # opções curtas
            self.setUp()
            args = (None, 'quina', '-n', str(i))
            readlines = run_script(args)
            linha = readlines[1]
            assert len([int(x) for x in linha.split()]) == i

            # opções longas
            self.setUp()
            args = (None, 'quina', '--numeros=%d' % i)
            readlines = run_script(args)
            linha = readlines[1]
            assert len([int(x) for x in linha.split()]) == i

    def test_gerar_VARIAS_apostas(self):
        # geração de apostas da quina padrão com 5 números
        args = (None, 'quina', '-q', '2')
        readlines = run_script(args)
        linhas = readlines[1:]
        assert len(linhas) == 2
        for no, linha in enumerate(linhas, 1):
            assert len([int(x) for x in linha.split()]) == 5

        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
            # opções curtas
            self.setUp()
            args = (None, 'quina', '-q', '2', '-n', str(i))
            readlines = run_script(args)
            linhas = readlines[1:]
            assert len(linhas) == 2
            for no, linha in enumerate(linhas, 1):
                assert len([int(x) for x in linha.split()]) == i

            # opções longas
            self.setUp()
            args = (None, 'quina', '--quantidade', '2', '--numeros=%d' % i)
            readlines = run_script(args)
            linhas = readlines[1:]
            assert len(linhas) == 2
            for no, linha in enumerate(linhas, 1):
                assert len([int(x) for x in linha.split()]) == i

    def test_consultar_UM_resultado(self):
        # consulta de apostas da quina
        args = (None, 'quina', '-c', '1')
        readlines = run_script(args)
        linhas = readlines[1:]
        assert linhas == ["quina:\n",
                          "  1: 25 45 60 76 79\n"]

    def test_consultar_VARIOS_resultados(self):
        # consulta de apostas da quina
        args = (None, 'quina', '-c', '1', '-c', '2')
        readlines = run_script(args)
        linhas = readlines[1:]
        assert linhas == ["quina:\n",
                          "  1: 25 45 60 76 79\n",
                          "  2: 13 30 58 63 64\n"]

    def test_conferir_UMA_aposta(self):
        args = (None, 'quina', '-c', '1', '1,25,39,44,76')
        readlines = run_script(args)
        linhas = readlines[1:]
        assert linhas == ["quina:\n",
                          "  1:\n",
                          "  - aposta: 01 25 39 44 76\n",
                          "    acertou:\n",
                          "      2: R$ 0,00\n"]

    def test_conferir_VARIAS_apostas(self):
        args = (None, 'quina', '-c', '1', '1,25,39,44,76', '25,39,45,66,76')
        readlines = run_script(args)
        linhas = readlines[1:6]
        assert linhas == ["quina:\n",
                          "  1:\n",
                          "  - aposta: 01 25 39 44 76\n",
                          "    acertou:\n",
                          "      2: R$ 0,00\n"]
        linhas = readlines[6:]
        assert linhas == ["  - aposta: 25 39 45 66 76\n",
                          "    acertou:\n",
                          "      3: R$ 42.982,00\n"]

    def test_conferir_apostas_em_VARIOS_concursos(self):
        args = (None, 'quina', '-c', '1', '-c', '2', '13,25,58,64,70')
        readlines = run_script(args)
        linhas = readlines[1:6]
        assert linhas == ["quina:\n",
                          "  1:\n",
                          "  - aposta: 13 25 58 64 70\n",
                          "    acertou:\n",
                          "      1: R$ 0,00\n"]
        linhas = readlines[6:]
        assert linhas == ["  2:\n",
                          "  - aposta: 13 25 58 64 70\n",
                          "    acertou:\n",
                          "      3: R$ 32.422,00\n"]
