import json
import random

from html.parser import HTMLParser

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
    },
    'megasena': {
        'marcar': (6, 15), 'numeros': (1, 60), 'nome': "Mega-Sena",
    },
    'lotofacil': {
        'marcar': (15, 18), 'numeros': (1, 25),
    },
    'lotomania': {
        'marcar': (1, 50), 'numeros': (1, 100), 'padrao': 20,
        'url-script': "_lotomania_pesquisa.asp",
    },
    'duplasena': {
        'marcar': (6, 15), 'numeros': (1, 50), 'nome': "Dupla Sena",
    },
}

class Loteria:
    def __init__(self, nome, cfg_path=None):
        nome = APELIDOS.get(nome, nome)
        try:
            c = LOTERIAS[nome]
        except KeyError as err:
            raise LoteriaNaoSuportada(err)

        self.settings = c
        self.nome = nome
        self.util = util.Util(cfg_path)
        self.loteria_db = self.util.get_mapdb('loteria')

        self._range = range(c['numeros'][0], c['numeros'][1] + 1)
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
        """Obtém o resultado do sorteio de um concurso.

        Primeiramente, é verificado se o resultado já existe em cache no banco de dados.
        Caso negativo, faz o download e armazena para uso futuro.
        """
        result = self._cache(concurso, com_premios)
        if result:
            return result

        result = self._download(concurso)
        self._store(result)

        return result

    def _cache(self, concurso, com_premios):
        result = self.loteria_db.get('%s|%s' % (self.nome, concurso))
        if result:
            def int_key(obj):
                return {(int(k) if k.isdecimal() else k):v for k, v in obj.items()}
            return json.loads(result, object_hook=int_key)

    def _download(self, concurso):
        parser = self._parser()
        if parser is None:
            raise NotImplementedError("parser")

        url = self._url(concurso)
        conteudo_html = self.util.download(url, in_cache=concurso > 0)

        parser.feed(conteudo_html)
        result = parser.data()

        if result is None:
            self.util.blame(url)
            raise ResultadoNaoDisponivel(self.nome, concurso)
        else:
            return result

    def _store(self, result):
        self.loteria_db['%s|%s' % (self.nome, result['concurso'])] = json.dumps(result)

    def conferir(self, concurso, apostas):
        result = self.consultar(concurso, com_premios=True)
        resp = []
        for aposta in apostas:
            acertou = [[n for n in res if n in aposta]
                       for res in result['numeros']]
            ganhou = self._ganhou(result, acertou)
            resp.append({
                'concurso': result['concurso'], 'numeros': aposta,
                'acertou': acertou,
                'ganhou': ganhou,
            })
        return resp

    def _ganhou(self, result, acertou):
        acertou = [len(t) for t in acertou]
        if self.nome == "duplasena" and acertou[0] == 6:
            acertou[0] = -6

        return [result['premios'].get(n, '0,00') for n in acertou]

    def _parser(self):
        if self.nome in ('quina', 'megasena', 'duplasena'):
            return LoteriaNewParser(self.nome)
        else:
            return LoteriaParser(self.nome)

    def _url(self, concurso,
             base="http://www1.caixa.gov.br/loterias/loterias/%(loteria)s/",
             script="%(loteria)s_pesquisa_new.asp",
             query="?submeteu=sim&opcao=concurso&txtConcurso=%(concurso)d"):
        script = self.settings.get('url-script', script)
        if concurso <= 0:
            return (base+script) % {'loteria': self.nome}
        else:
            return (base+script+query) % {'loteria': self.nome,
                                          'concurso': concurso}


class LoteriaParser(HTMLParser):
    SPECS = {
        'quina': {
            'numeros': [(21, 25)],
            'premios': {
                5: 7,
                4: 9,
                3: 11,
            },
        },
        'megasena': {
            'numeros': [(28, 33)],
            'premios': {
                6: 11,
                5: 13,
                4: 15,
            },
        },
        'lotofacil': {
            'numeros': [(3, 17)],
            'premios': {
                15: 19,
                14: 21,
                13: 23,
                12: 25,
                11: 27,
            },
        },
        'lotomania': {
            'numeros': [(6, 25)],
            'premios': {
                20: 28,
                19: 30,
                18: 32,
                17: 34,
                16: 36,
                0: 38,
            },
        },
        'duplasena': {
            'numeros': [(4, 9), (12, 17)],
            'premios': {
                -6: 21,
                6: 24,
                5: 25,
                4: 27,
            },
        },
    }

    def __init__(self, nome, *, convert_charrefs=True):
        self._spec = self.SPECS.get(nome)
        if self._spec is None:
            raise NotImplementedError("spec")
        if 'premios' not in self._spec:
            raise NotImplementedError("spec[premios]")

        super().__init__(convert_charrefs=convert_charrefs)
        self.reset(init=True)

    def data(self):
        spec = self._spec
        dados = ''.join(self._data).split('|')

        pos_nums = [range(p[0], p[1] + 1) for p in spec['numeros']]
        try:
            premios = {}
            for qnt, pos_premio in sorted(spec['premios'].items()):
                premios[qnt] = dados[pos_premio]

            return {
                'concurso': int(dados[spec.get('concurso', 0)]),
                'numeros': [[int(dados[i]) for i in r] for r in pos_nums],
                'premios': premios,
            }
        except (IndexError, ValueError):
            return None

    def reset(self, init=False):
        if not init:
            super().reset()

        self._capture = True
        self._data = []

    def handle_starttag(self, tag, attrs):
        self._capture = False

    def handle_endtag(self, tag):
        self._capture = True

    def handle_data(self, data):
        if self._capture:
            self._data.append(data)

    def error(self, message):
        raise RuntimeError(message)


class LoteriaNewParser(LoteriaParser):
    def reset(self, **kwargs):
        super().reset(**kwargs)

        self._capture_list = False
        self._capture_number = False
        self._numbers = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)

        if tag == "ul":
            self._capture_list = True

        elif tag == "li" and self._capture_list:
            self._capture_number = True

    def handle_endtag(self, tag):
        super().handle_endtag(tag)

        if tag == "li" and self._capture_list:
            self._capture_number = False

        elif tag == "ul" and len(self._numbers) > 0:
            self._data.append('|' + '|'.join(self._numbers) + '|')
            self._capture_list = False
            self._numbers = []

    def handle_data(self, data):
        super().handle_data(data)

        if self._capture_number:
            self._numbers.append(data)
