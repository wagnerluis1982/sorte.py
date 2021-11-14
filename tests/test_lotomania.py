# encoding=utf8

import basetest


class LotomaniaTest(basetest.LoteriaTestCase):
    # atributos do teste 'gerar aposta'
    nome = "lotomania"
    permitidos = set(range(1, 101))  # de 1 a 100
    numeros = (20, 5, 7, 10, 15, 20, 30, 40, 45)

    # atributos do teste 'consultar resultado'
    concurso = 1
    sorteios = [
        [6, 11, 14, 16, 21, 22, 25, 32, 33, 34, 46, 61, 70, 73, 78, 88, 89, 90, 95, 0]
    ]

    # atributos do teste 'conferir aposta'
    apostas = [
        [4, 11, 16, 25, 29, 30, 33, 39, 41, 44, 47, 52, 59, 62, 77, 80, 85, 88, 90, 99],
        [
            6,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            25,
            28,
            29,
            30,
            31,
            46,
            70,
            73,
            78,
            88,
            89,
            90,
            95,
            0,
        ],
    ]
    esperados = {
        "acertou": (
            [[11, 16, 25, 33, 88, 90]],
            [[6, 11, 14, 16, 21, 22, 25, 46, 70, 73, 78, 88, 89, 90, 95, 0]],
        ),
        "ganhou": (["0,00"], ["21,78"]),
    }
