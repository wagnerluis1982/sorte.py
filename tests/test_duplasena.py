# encoding=utf8

import basetest

class DuplaSenaTest(basetest.LoteriaTestCase):
    'Dupla Sena'

    nome = "duplasena"
    permitidos = set(range(1, 51))  # de 1 a 50
    numeros = range(6, 16)  # de 6 a 15
