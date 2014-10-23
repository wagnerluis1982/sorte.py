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
        'resultado': {'numeros': (21, 25)},
    },
    'megasena': {'marcar': (6, 15), 'numeros': (1, 60), 'nome': "Mega-Sena"},
    'lotofacil': {'marcar': (15, 18), 'numeros': (1, 25)},
    'lotomania': {'marcar': (1, 50), 'numeros': (1, 100), 'padrao': 20},
    'duplasena': {'marcar': (6, 15), 'numeros': (1, 50), 'nome': "Dupla Sena"},
}

class Loteria:
    def __init__(self, nome):
        try:
            c = LOTERIAS[APELIDOS.get(nome, nome)]
        except KeyError, err:
            raise LoteriaNaoSuportada(err.message)

        self.settings = c
        self.nome = nome
        self.util = util.Util()

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

    def consultar(self, concurso=0):
        parser = self._parser()
        if parser is None:
            raise LoteriaNaoSuportada(self.nome)

        posicao = self.settings.get('resultado')
        if posicao is None:
            raise LoteriaNaoSuportada(self.nome)

        url = self._url(concurso)
        conteudo_html = self.util.download(url, in_cache=concurso > 0)
        parser.feed(conteudo_html)

        dados = parser.data()
        pos_numeros = xrange(posicao['numeros'][0], posicao['numeros'][1]+1)
        try:
            result = {
                'concurso': int(dados[posicao.get('concurso', 0)]),
                'numeros': [int(dados[i]) for i in pos_numeros],
            }
            return result
        except ValueError:
            self.util.cache_evict(url)
            raise ResultadoNaoDisponivel(self.nome, concurso)


    def _parser(self):
        if self.nome == 'quina':
            return QuinaParser()
        else:
            return None

    def _url(self, concurso,
             base="http://www1.caixa.gov.br/loterias/loterias/%(loteria)s/",
             script="%(loteria)s_pesquisa_new.asp",
             query="?submeteu=sim&opcao=concurso&txtConcurso=%(concurso)d"):
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
