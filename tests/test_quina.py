# encoding=utf8

import basetest

class QuinaTest(basetest.LoteriaTestCase):
    # atributos do teste 'gerar aposta'
    nome = "quina"
    permitidos = set(range(1, 81))  # de 1 a 80
    numeros = (5, 6, 7)

    def test_consultar_resultado(_):
        result = _.loto.consultar(1)
        _.is_instance(result, dict)
        _.eq(result['concurso'], 1)
        _.eq(result['numeros'], [[25, 45, 60, 76, 79]])
