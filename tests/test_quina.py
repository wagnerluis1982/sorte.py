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

    def test_conferir_aposta(_):
        aposta = [1, 25, 39, 44, 76]
        resp = _.loto.conferir(_.concurso, aposta)
        _.is_instance(resp, dict)
        _.eq(resp['concurso'], _.concurso)
        _.eq(resp['numeros'], aposta)
        _.eq(resp['acertou'], 2)
        _.eq(resp['ganhou'], '0,00')

        aposta = [25, 39, 45, 76, 79]
        resp = _.loto.conferir(_.concurso, aposta)
        _.is_instance(resp, dict)
        _.eq(resp['concurso'], _.concurso)
        _.eq(resp['numeros'], aposta)
        _.eq(resp['acertou'], 4)
        _.eq(resp['ganhou'], '1.788.927,00')
