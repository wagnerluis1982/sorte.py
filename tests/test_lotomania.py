# encoding=utf8

import basetest

class LotomaniaTest(basetest.LoteriaTestCase):
    nome = "lotomania"
    permitidos = set(range(1, 101))  # de 1 a 100
    numeros = (20, 5, 7, 10, 15, 20, 30, 40, 45)
