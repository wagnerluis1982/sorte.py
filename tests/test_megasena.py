# encoding=utf8

import basetest

class MegaSenaTest(basetest.LoteriaTestCase):
    'Mega-Sena'

    nome = "megasena"
    permitidos = set(range(1, 61))  # de 1 a 60
    numeros = range(6, 16)  # de 6 a 15

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[4, 5, 30, 33, 41, 52]]
