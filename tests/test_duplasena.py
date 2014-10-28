# encoding=utf8

import basetest

class DuplaSenaTest(basetest.LoteriaTestCase):
    'Dupla Sena'

    # atributos do teste 'gerar aposta'
    nome = "duplasena"
    permitidos = set(range(1, 51))  # de 1 a 50
    numeros = range(6, 16)  # de 6 a 15

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[7, 15, 24, 41, 48, 50], [9, 37, 41, 43, 44, 49]]

    # atributos do teste 'conferir aposta'
    apostas = [[1, 7, 41, 48, 50], [25, 39, 44, 76, 79]]
    esperados = {'acertou': ([4, 1], [0, 1]),
                 'ganhou': (['97,16', '0,00'], ['0,00', '0,00'])}
