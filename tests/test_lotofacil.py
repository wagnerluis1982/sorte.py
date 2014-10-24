# encoding=utf8

import basetest

class LotofacilTest(basetest.LoteriaTestCase):
    nome = "lotofacil"
    permitidos = set(range(1, 26))  # de 1 a 25
    numeros = range(15, 19)  # de 15 a 18
