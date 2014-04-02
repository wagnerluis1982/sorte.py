import random

class QuantidadeInvalida(Exception):
    def __init__(self, valor):
        self.valor = valor
        Exception.__init__(self, valor)

class Loteria:
    def __init__(self, nome):
        pass

    def gerar_aposta(self, quant=None):
        if quant is None:
            quant = 5
        if not (5 <= quant <= 80):
            raise QuantidadeInvalida(quant)
        result = random.sample(xrange(1, 81), quant)
        return tuple(sorted(result))
