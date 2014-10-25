# encoding=utf8

import basetest

class QuinaTest(basetest.LoteriaTestCase):
    # atributos do teste 'gerar aposta'
    nome = "quina"
    permitidos = set(range(1, 81))  # de 1 a 80
    numeros = (5, 6, 7)

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [[25, 45, 60, 76, 79]]
