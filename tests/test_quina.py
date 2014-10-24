# encoding=utf8

import basetest

class QuinaTest(basetest.LoteriaTestCase):
    nome = "quina"
    permitidos = set(range(1, 81))  # de 1 a 80
    numeros = (5, 6, 7)
