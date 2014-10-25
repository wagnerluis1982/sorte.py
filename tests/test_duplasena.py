# encoding=utf8

import basetest

class DuplaSenaTest(basetest.LoteriaTestCase):
    'Dupla Sena'

    nome = "duplasena"
    permitidos = set(range(1, 51))  # de 1 a 50
    numeros = range(6, 16)  # de 6 a 15

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[7, 15, 24, 41, 48, 50], [9, 37, 41, 43, 44, 49]]
