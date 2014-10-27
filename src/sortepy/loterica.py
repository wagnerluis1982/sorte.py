import random

from HTMLParser import HTMLParser

from . import util


class LoteriaNaoSuportada(Exception):
    pass


class QuantidadeInvalida(Exception):
    pass


class ResultadoNaoDisponivel(Exception):
    pass


APELIDOS = {
    'sena': 'megasena',
}

LOTERIAS = {
    'quina': {
        'marcar': (5, 7), 'numeros': (1, 80),
        'resultado': {
            'numeros': [(21, 25)],
            'premios': {
                5: 7,
                4: 9,
                3: 11,
            },
        },
    },
    'megasena': {
        'marcar': (6, 15), 'numeros': (1, 60), 'nome': "Mega-Sena",
        'resultado': {
            'numeros': [(28, 33)],
        },
    },
    'lotofacil': {
        'marcar': (15, 18), 'numeros': (1, 25),
        'resultado': {
            'numeros': [(3, 17)],
        },
    },
    'lotomania': {
        'marcar': (1, 50), 'numeros': (1, 100), 'padrao': 20,
        'resultado': {
            'numeros': [(6, 25)], 'url-script': "_lotomania_pesquisa.asp",
        },
    },
    'duplasena': {
        'marcar': (6, 15), 'numeros': (1, 50), 'nome': "Dupla Sena",
        'resultado': {
            'numeros': [(4, 9), (12, 17)],
            'premios': {
                -6: 21,
                6: 24,
                5: 25,
                4: 27,
            },
        },
    },
}

class Loteria:
    def __init__(self, nome, cfg_path=None):
        nome = APELIDOS.get(nome, nome)
        try:
            c = LOTERIAS[nome]
        except KeyError, err:
            raise LoteriaNaoSuportada(err.message)

        self.settings = c
        self.nome = nome
        self.util = util.Util(cfg_path)

        self._range = xrange(c['numeros'][0], c['numeros'][1] + 1)
        self._min = c['marcar'][0]
        self._max = c['marcar'][1]
        self._padrao = c.get('padrao', self._min)

    def gerar_aposta(self, marcar=None):
        if marcar is None:
            marcar = self._padrao
        if not (self._min <= marcar <= self._max):
            raise QuantidadeInvalida(self.nome, marcar)
        result = random.sample(self._range, marcar)
        return tuple(sorted(result))

    def consultar(self, concurso=0, com_premios=False):
        parser = self._parser()
        if parser is None:
            raise LoteriaNaoSuportada(self.nome)

        posicao = self.settings.get('resultado')
        if posicao is None:
            raise LoteriaNaoSuportada(self.nome)

        if com_premios and posicao.get('premios') is None:
            raise LoteriaNaoSuportada(self.nome)

        url = self._url(concurso)
        conteudo_html = self.util.download(url, in_cache=concurso > 0)
        parser.feed(conteudo_html)

        pos_nums = [xrange(p[0], p[1]+1) for p in posicao['numeros']]
        dados = parser.data()
        try:
            result = {
                'concurso': int(dados[posicao.get('concurso', 0)]),
                'numeros': [[int(dados[i]) for i in r] for r in pos_nums],
            }
            if com_premios:
                result['premios'] = {}
                for qnt, pos_premio in sorted(posicao['premios'].items()):
                    result['premios'][qnt] = dados[pos_premio]
            return result
        except ValueError:
            self.util.cache_evict(url)
            raise ResultadoNaoDisponivel(self.nome, concurso)

    def conferir(self, concurso, apostas):
        result = self.consultar(concurso, com_premios=True)
        resp = []
        for aposta in apostas:
            acertou = [len([1 for n in res if n in aposta])
                       for res in result['numeros']]
            ganhou = self._ganhou(result, acertou[:])
            resp.append({
                'concurso': result['concurso'], 'numeros': aposta,
                'acertou': acertou,
                'ganhou': ganhou,
            })
        return resp

    def _ganhou(self, result, acertou):
        if self.nome == "duplasena" and acertou[0] == 6:
            acertou[0] = -6

        return [result['premios'].get(n, '0,00') for n in acertou]

    def _parser(self):
        if self.nome in ('quina', 'megasena', 'duplasena'):
            return QuinaParser()
        else:
            return LoteriaParser()

    def _url(self, concurso,
             base="http://www1.caixa.gov.br/loterias/loterias/%(loteria)s/",
             script="%(loteria)s_pesquisa_new.asp",
             query="?submeteu=sim&opcao=concurso&txtConcurso=%(concurso)d"):
        script = self.settings['resultado'].get('url-script', script)
        if concurso <= 0:
            return (base+script) % {'loteria': self.nome}
        else:
            return (base+script+query) % {'loteria': self.nome,
                                          'concurso': concurso}


class LoteriaParser(HTMLParser):
    def data(self):
        return ''.join(self._data).split('|')

    def reset(self):
        HTMLParser.reset(self)

        self._capture = True
        self._data = []

    def handle_starttag(self, tag, attrs):
        self._capture = False

    def handle_endtag(self, tag):
        self._capture = True

    def handle_data(self, data):
        if self._capture:
            self._data.append(data)


class QuinaParser(LoteriaParser):
    def reset(self):
        LoteriaParser.reset(self)

        self._capture_list = False
        self._capture_number = False
        self._numbers = []

    def handle_starttag(self, tag, attrs):
        LoteriaParser.handle_starttag(self, tag, attrs)

        if tag == "li":
            self._capture_number = True

        if tag == "ul":
            self._capture_list = True

    def handle_endtag(self, tag):
        LoteriaParser.handle_endtag(self, tag)

        if tag == "li":
            self._capture_number = False

        if tag == "ul" and self._capture_list and len(self._numbers) > 0:
            self._data.append('|' + '|'.join(self._numbers) + '|')
            self._numbers = []

    def handle_data(self, data):
        LoteriaParser.handle_data(self, data)

        if self._capture_number:
            self._numbers.append(data)
