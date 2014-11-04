# encoding=utf8

import basetest

class QuinaTest(basetest.LoteriaTestCase):
    # atributos do teste 'gerar aposta'
    nome = "quina"
    permitidos = set(range(1, 81))  # de 1 a 80
    numeros = (5, 6, 7)

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[25, 45, 60, 76, 79]]

    # atributos do teste 'conferir aposta'
    apostas = [[1, 25, 39, 44, 76], [25, 39, 45, 76, 79]]
    esperados = {'acertou': ([[25, 76]], [[25, 45, 76, 79]]),
                 'ganhou': (['0,00'], ['1.788.927,00'])}
