# encoding=utf8

import basetest

from sortepy.script import main

# Os testes do script são focados na loteria da Quina porque tem menos números
# para verificar. Caso necessário, testes com outras loterias serão criados.
# Como todas as loterias possuem testes individuais, isto não é um grande
# problema.
class ScriptTest(basetest.BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = FakeStdOut()

    def setUp(self):
        self.output.clear()

    def test_gerar_UMA_aposta_padrao(_):
        # geração de aposta da quina padrão com 5 números
        args = (None, 'quina')
        main(args, stdout=_.output)
        linha = _.output.line(2)
        _.eq(len([int(x) for x in linha.split()]), 5)

    def test_gerar_UMA_aposta_nao_padrao(_):
        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
            # opções curtas
            _.output.clear()
            args = (None, 'quina', '-n', str(i))
            main(args, stdout=_.output)
            linha = _.output.line(2)
            _.eq(len([int(x) for x in linha.split()]), i)

            # opções longas
            _.output.clear()
            args = (None, 'quina', '--numeros=%d' % i)
            main(args, stdout=_.output)
            linha = _.output.line(2)
            _.eq(len([int(x) for x in linha.split()]), i)

    def test_gerar_VARIAS_apostas(_):
        # geração de apostas da quina padrão com 5 números
        args = (None, 'quina', '-q', '2')
        main(args, stdout=_.output)
        linhas = _.output.lines(2, 3)
        for no, linha in enumerate(linhas, 1):
            _.eq(len([int(x) for x in linha.split()]), 5)

        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
            # opções curtas
            _.output.clear()
            args = (None, 'quina', '-q', '2', '-n', str(i))
            main(args, stdout=_.output)
            linhas = _.output.lines(2, 3)
            for no, linha in enumerate(linhas, 1):
                _.eq(len([int(x) for x in linha.split()]), i)

            # opções longas
            _.output.clear()
            args = (None, 'quina', '--quantidade', '2', '--numeros=%d' % i)
            main(args, stdout=_.output)
            linhas = _.output.lines(2, 3)
            for no, linha in enumerate(linhas, 1):
                _.eq(len([int(x) for x in linha.split()]), i)

    def test_consultar_UM_resultado(_):
        # consulta de apostas da quina
        args = (None, 'quina', '-c', '1')
        main(args, stdout=_.output, cfg_path=basetest.cfg_fixture_path)
        linhas = _.output.lines(2, 3)
        _.eq(linhas, ["quina:\n",
                      "  1: 25 45 60 76 79\n"])

    def test_consultar_VARIOS_resultados(_):
        # consulta de apostas da quina
        args = (None, 'quina', '-c', '1', '-c', '2')
        main(args, stdout=_.output, cfg_path=basetest.cfg_fixture_path)
        linhas = _.output.lines(2, 4)
        _.eq(linhas, ["quina:\n",
                      "  1: 25 45 60 76 79\n",
                      "  2: 13 30 58 63 64\n"])

    def test_conferir_UMA_aposta(_):
        args = (None, 'quina', '-c', '1', '1,25,39,44,76')
        main(args, stdout=_.output, cfg_path=basetest.cfg_fixture_path)
        linhas = _.output.lines(2, 6)
        _.eq(linhas, ["quina:\n",
                      "  1:\n",
                      "  - aposta: 01 25 39 44 76\n",
                      "    acertou:\n",
                      "      2: R$ 0,00\n"])

    def test_conferir_VARIAS_apostas(_):
        args = (None, 'quina', '-c', '1', '1,25,39,44,76', '25,39,45,66,76')
        main(args, stdout=_.output, cfg_path=basetest.cfg_fixture_path)
        linhas = _.output.lines(2, 6)
        _.eq(linhas, ["quina:\n",
                      "  1:\n",
                      "  - aposta: 01 25 39 44 76\n",
                      "    acertou:\n",
                      "      2: R$ 0,00\n"])
        linhas = _.output.lines(7, 9)
        _.eq(linhas, ["  - aposta: 25 39 45 66 76\n",
                      "    acertou:\n",
                      "      3: R$ 42.982,00\n"])

    def test_conferir_apostas_em_VARIOS_concursos(_):
        args = (None, 'quina', '-c', '1', '-c', '2', '13,25,58,64,70')
        main(args, stdout=_.output, cfg_path=basetest.cfg_fixture_path)
        linhas = _.output.lines(2, 6)
        _.eq(linhas, ["quina:\n",
                      "  1:\n",
                      "  - aposta: 13 25 58 64 70\n",
                      "    acertou:\n",
                      "      1: R$ 0,00\n"])
        linhas = _.output.lines(7, 10)
        _.eq(linhas, ["  2:\n",
                      "  - aposta: 13 25 58 64 70\n",
                      "    acertou:\n",
                      "      3: R$ 32.422,00\n"])


class FakeStdOut:
    def __init__(self):
        self.buf = []

    def write(self, s):
        buf = self.buf
        lines = s.splitlines(True)
        if lines:
            if buf and not buf[-1].endswith('\n'):
                buf[-1] += lines[0]
                buf.extend(lines[1:])
            else:
                buf.extend(lines)

    def isatty(self):
        return False

    def clear(self):
        del self.buf[:]

    def line(self, i):
        buf = self.buf
        assert 1 <= i <= len(buf), "linha %d fora da faixa" % i
        return buf[i-1]

    def lines(self, i, j):
        buf = self.buf
        assert 1 <= i <= len(buf), "linha %d fora da faixa" % i
        assert 1 <= j <= len(buf), "linha %d fora da faixa" % i
        assert i <= j, 'i=%d > j=%d' % (i, j)
        return buf[i-1:j]
