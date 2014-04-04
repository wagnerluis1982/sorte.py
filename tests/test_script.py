# encoding=utf8

import basetest

from StringIO import StringIO
from sortepy.script import main

# Os testes do script serão focados na loteria da Quina porque tem menos números
# para verificar. Caso necessário, testes com outras loterias serão criados.
class ScriptTest(basetest.BaseTestCase):
    @classmethod
    def setUpClass(cls):
        global output
        output = FakeStdOut()

    def setUp(_):
        output.clear()

    def test_gerar_UMA_aposta_padrao(_):
        # geração de aposta da quina padrão com 5 números
        args = (None, 'quina')
        main(args, stdout=output)
        linha = output.line(2)
        _.eq(len([int(x) for x in linha.split()]), 5)

    def test_gerar_UMA_aposta_nao_padrao(_):
        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
        # opções curtas
            output.clear()
            args = (None, 'quina', '-n', str(i))
            main(args, stdout=output)
            linha = output.line(2)
            _.eq(len([int(x) for x in linha.split()]), i)
        # opções longas
            output.clear()
            args = (None, 'quina', '--numeros=%d' % i)
            main(args, stdout=output)
            linha = output.line(2)
            _.eq(len([int(x) for x in linha.split()]), i)

    def test_gerar_VARIAS_apostas(_):
        # geração de apostas da quina padrão com 5 números
        args = (None, 'quina', '-q', '2')
        main(args, stdout=output)
        linhas = output.lines(2, 3)
        for no, linha in enumerate(linhas, 1):
            _.eq(linha[0:2], '#%d' % no)
            _.eq(len([int(x) for x in linha[5:].split()]), 5)

        # geração de aposta da quina com mais de 5 números
        for i in (6, 7):
        # opções curtas
            output.clear()
            args = (None, 'quina', '-q', '2', '-n', str(i))
            main(args, stdout=output)
            linhas = output.lines(2, 3)
            for no, linha in enumerate(linhas, 1):
                _.eq(linha[0:2], '#%d' % no)
                _.eq(len([int(x) for x in linha[5:].split()]), i)
        # opções longas
            output.clear()
            args = (None, 'quina', '--quantidade', '2', '--numeros=%d' % i)
            main(args, stdout=output)
            linhas = output.lines(2, 3)
            for no, linha in enumerate(linhas, 1):
                _.eq(linha[0:2], '#%d' % no)
                _.eq(len([int(x) for x in linha[5:].split()]), i)


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
        assert i <= j, 'i=%d > j=%d' (i, j)
        return buf[i-1:j]
