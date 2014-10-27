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

    def test_conferir_aposta(_):
        apostas = [[1, 7, 41, 48, 50]]
        resp = _.loto.conferir(_.concurso, apostas)
        _.is_instance(resp, list)
        _.eq(resp[0]['concurso'], _.concurso)
        _.eq(resp[0]['numeros'], apostas[0])
        _.eq(resp[0]['acertou'], [4, 1])
        _.eq(resp[0]['ganhou'], ['97,16', '0,00'])

    def test_conferir_varias_apostas(_):
        apostas = [[1, 7, 41, 48, 50], [25, 39, 44, 76, 79]]
        resp = _.loto.conferir(_.concurso, apostas)
        esperados = {'acertou': ([4, 1], [0, 1]),
                     'ganhou': (['97,16', '0,00'], ['0,00', '0,00'])}
        _.is_instance(resp, list)
        for i in range(len(apostas)):
            _.eq(resp[i]['concurso'], _.concurso)
            _.eq(resp[i]['numeros'], apostas[i])
            _.eq(resp[i]['acertou'], esperados['acertou'][i])
            _.eq(resp[i]['ganhou'], esperados['ganhou'][i])
