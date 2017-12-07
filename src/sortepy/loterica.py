import collections
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


# tipos de loteria
K_COMMON = 0
K_TICKET = 1

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
    'federal': {
        # essa loteria não gera números
        'url-script': "federal_pesquisa.asp",
        'kind': K_TICKET,
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

        # Se for uma loteria do tipo TICKET. não há gerador, assim substitui
        # método `gerar_aposta()` e encerra.
        self._kind = c.get('kind', K_COMMON)
        if self._kind == K_TICKET:
            self.gerar_aposta = lambda *a, **k: None
            return

        # atributos do gerador de números
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

            # convert `(k, v)` de volta para `dict`
            result = json.loads(result, object_hook=int_key)
            result['premios'] = collections.OrderedDict(result['premios'])

            return result

    def _download(self, concurso):
        parser = LoteriaParser(self.nome)

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
        # converte `dict` para `(k, v)`: garante os prêmios na ordem devolvida pelo parser
        result = result.copy()
        result['premios'] = list(result['premios'].items())
        # armazena no cache
        self.loteria_db['%s|%s' % (self.nome, result['concurso'])] = json.dumps(result)

    def conferir(self, concurso, apostas):
        result = self.consultar(concurso, com_premios=True)
        resp = []
        for aposta in apostas:
            if self._kind == K_COMMON:
                acertou = [[n for n in res if n in aposta]
                           for res in result['numeros']]
            else:
                acertou = [aposta for res in result['premios'] if [res] == aposta]

            ganhou = self._ganhou(result, acertou)
            resp.append({
                'concurso': result['concurso'], 'numeros': aposta,
                'acertou': acertou,
                'ganhou': ganhou,
            })
        return resp

    def _ganhou(self, result, acertou):
        if self._kind == K_COMMON:
            acertou = [len(t) for t in acertou]
            if self.nome == "duplasena" and acertou[0] == 6:
                acertou[0] = -6
        else:
            acertou = [v for [v] in acertou] or [None]

        return [result['premios'].get(n, '0,00') for n in acertou]

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


class LoteriaParser:
    NEW = 1
    SPECS = {
        'quina': {
            'numeros': [(21, 25)],
            'premios': {
                5: 7,
                4: 9,
                3: 11,
            },
            'parser': NEW,
        },
        'megasena': {
            'numeros': [(28, 33)],
            'premios': {
                6: 11,
                5: 13,
                4: 15,
            },
            'parser': NEW,
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
            'parser': NEW,
        },
        'federal': {
            'concurso': 2,
            'numeros': (6, 8, 10, 12, 14),
            'premios': (7, 9, 11, 13, 15),
            'kind': K_TICKET,
        },
    }

    def __init__(self, nome):
        self._spec = self.SPECS.get(nome)
        if self._spec is None:
            raise NotImplementedError("parser")
        if 'premios' not in self._spec:
            raise NotImplementedError("parser: premios")

        if self._spec.get('parser') == self.NEW:
            self._parser = _NewParser()
        else:
            self._parser = _OldParser()

    def __getattr__(self, name):
        return getattr(self._parser, name)

    def data(self):
        spec = self._spec
        dados = ''.join(self._parser.data).split('|')

        kind = spec.get('kind', K_COMMON)
        if kind == K_COMMON:
            subdados = self.__common(spec, dados)
        else:
            subdados = self.__ticket(spec, dados)

        if subdados:
            numeros, premios = subdados
        else:
            return None

        return {
            'concurso': int(dados[spec.get('concurso', 0)]),
            'numeros': numeros,
            'premios': premios,
        }

    @staticmethod
    def __common(spec, dados):
        pos_nums = [range(p[0], p[1] + 1) for p in spec['numeros']]
        try:
            numeros = [[int(dados[i]) for i in r] for r in pos_nums]
            premios = collections.OrderedDict()
            for qnt, pos_premio in sorted(spec['premios'].items(), reverse=True):
                premios[qnt] = dados[pos_premio]

            return numeros, premios
        except (IndexError, ValueError):
            return None

    @staticmethod
    def __ticket(spec, dados):
        try:
            premios = collections.OrderedDict()
            for pos_ticket, pos_premio in zip(spec['numeros'], spec['premios']):
                ticket = int(dados[pos_ticket].replace('.', ''))
                premios[ticket] = dados[pos_premio]

            return None, premios
        except (IndexError, ValueError):
            return None


class _OldParser(HTMLParser):
    @property
    def data(self):
        return self._data

    def reset(self):
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


class _NewParser(_OldParser):
    def reset(self):
        super().reset()

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
