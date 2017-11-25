# encoding=utf8

import basetest

class LotofacilTest(basetest.LoteriaTestCase):
    # atributos do teste 'gerar aposta'
    nome = "lotofacil"
    permitidos = set(range(1, 26))  # de 1 a 25
    numeros = list(range(15, 19))  # de 15 a 18

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[2, 3, 5, 6, 9, 10, 11, 13, 14, 16, 18, 20, 23, 24, 25]]

    # atributos do teste 'conferir aposta'
    apostas = [[1, 2, 4, 6, 7, 9, 10, 11, 12, 14, 15, 17, 23, 24, 25],
               [2, 3, 5, 6, 9, 10, 11, 13, 14, 16, 18, 20, 23, 24, 25]]
    esperados = {'acertou': ([[2, 6, 9, 10, 11, 14, 23, 24, 25]],
                             [[2, 3, 5, 6, 9, 10, 11, 13, 14, 16, 18, 20, 23,
                               24, 25]]),
                 'ganhou': (['0,00'], ['49.765,82'])}
