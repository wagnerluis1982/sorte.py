import random

class LoteriaNaoSuportada(Exception):
    def __init__(self, nome):
        self.nome = nome
        Exception.__init__(self, nome)

class QuantidadeInvalida(Exception):
    def __init__(self, valor):
        self.valor = valor
        Exception.__init__(self, valor)


APELIDOS = {
    'sena': 'megasena',
}

LOTERIAS = {
    'quina': {'numeros': (5, 7), 'faixa': (1, 80)},
    'megasena': {'numeros': (6, 15), 'faixa': (1, 60), 'nome': "Mega-Sena"},
    'lotofacil': {'numeros': (15, 18), 'faixa': (1, 25)},
    'lotomania': {'numeros': (1, 50), 'faixa': (1, 100), 'padrao': 20},
    'duplasena': {'numeros': (6, 15), 'faixa': (1, 50), 'nome': "Dupla Sena"},
}

class Loteria:
    def __init__(self, nome):
        try:
            c = LOTERIAS[APELIDOS.get(nome, nome)]
        except KeyError, err:
            raise LoteriaNaoSuportada(err.message)
        else:
            quant = c['numeros']
            faixa = c['faixa']
            self.nome = c.get('nome', nome.title())
            self.qmin = quant[0]
            self.qmax = quant[1]
            self.padrao = c.get('padrao', self.qmin)
            self.range = xrange(faixa[0], faixa[1] + 1)

    def gerar_aposta(self, quant=None):
        if quant is None:
            quant = self.padrao
        if not (self.qmin <= quant <= self.qmax):
            raise QuantidadeInvalida(quant)
        result = random.sample(self.range, quant)
        return tuple(sorted(result))
