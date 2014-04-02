import random

class LoteriaNaoSuportada(Exception):
    def __init__(self, nome):
        self.nome = nome
        Exception.__init__(self, nome)

class QuantidadeInvalida(Exception):
    def __init__(self, valor):
        self.valor = valor
        Exception.__init__(self, valor)


LOTERIAS = {
    'quina': {'validos': (5, 80), 'faixa': (1, 80)},
}

class Loteria:
    def __init__(self, nome):
        try:
            c = LOTERIAS[nome]
        except KeyError, err:
            raise LoteriaNaoSuportada(err.message)
        else:
            self.qmin = c['validos'][0]
            self.qmax = c['validos'][1]
            self.range = xrange(c['faixa'][0], c['faixa'][1] + 1)

    def gerar_aposta(self, quant=None):
        qmin, qmax = self.qmin, self.qmax
        if quant is None:
            quant = qmin
        if not (qmin <= quant <= qmax):
            raise QuantidadeInvalida(quant)
        result = random.sample(self.range, quant)
        return tuple(sorted(result))
