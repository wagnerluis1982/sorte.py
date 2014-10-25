# encoding=utf8

import basetest

class LotofacilTest(basetest.LoteriaTestCase):
    nome = "lotofacil"
    permitidos = set(range(1, 26))  # de 1 a 25
    numeros = range(15, 19)  # de 15 a 18

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[2, 3, 5, 6, 9, 10, 11, 13, 14, 16, 18, 20, 23, 24, 25]]
