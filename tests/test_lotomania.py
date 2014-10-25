# encoding=utf8

import basetest

class LotomaniaTest(basetest.LoteriaTestCase):
    nome = "lotomania"
    permitidos = set(range(1, 101))  # de 1 a 100
    numeros = (20, 5, 7, 10, 15, 20, 30, 40, 45)

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[6, 11, 14, 16, 21, 22, 25, 32, 33, 34,
                 46, 61, 70, 73, 78, 88, 89, 90, 95, 0]]
