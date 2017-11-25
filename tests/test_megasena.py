# encoding=utf8

import basetest

class MegaSenaTest(basetest.LoteriaTestCase):
    'Mega Sena'

    # atributos do teste 'gerar aposta'
    nome = "megasena"
    permitidos = set(range(1, 61))  # de 1 a 60
    numeros = list(range(6, 16))  # de 6 a 15

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[4, 5, 30, 33, 41, 52]]

    # atributos do teste 'conferir aposta'
    apostas = [[4, 25, 30, 41, 52, 59], [25, 39, 45, 50, 51, 52]]
    esperados = {'acertou': ([[4, 30, 41, 52]], [[52]]),
                 'ganhou': (['330,21'], ['0,00'])}
