import collections
import json
import random

from abc import ABCMeta
from abc import abstractmethod
from html.parser import HTMLParser
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from sortepy import util


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
    "sena": "megasena",
}

LOTERIAS: Dict[str, Dict[str, Any]] = {
    "quina": {
        "marcar": (5, 7),
        "numeros": (1, 80),
    },
    "megasena": {
        "marcar": (6, 15),
        "numeros": (1, 60),
        "nome": "Mega-Sena",
    },
    "lotofacil": {
        "marcar": (15, 18),
        "numeros": (1, 25),
    },
    "lotomania": {
        "marcar": (1, 50),
        "numeros": (1, 100),
        "padrao": 20,
        "url-script": "_lotomania_pesquisa.asp",
    },
    "duplasena": {
        "marcar": (6, 15),
        "numeros": (1, 50),
        "nome": "Dupla Sena",
    },
    "federal": {
        # essa loteria não gera números
        "url-script": "federal_pesquisa.asp",
        "kind": K_TICKET,
    },
}


class Loteria:
    kind = property(lambda self: self._kind)

    def __init__(self, nome: str, cfg_path: str = None):
        nome = APELIDOS.get(nome, nome)
        try:
            self.settings: Dict[str, Any] = LOTERIAS[nome]
        except KeyError as err:
            raise LoteriaNaoSuportada(err)

        self.nome = nome
        self.util = util.Util(cfg_path)
        self.loteria_db = self.util.get_mapdb("loteria")

        # Se for uma loteria do tipo TICKET. não há gerador, assim substitui
        # método `gerar_aposta()` e encerra.
        self._kind = self.settings.get("kind", K_COMMON)
        if self._kind == K_TICKET:
            self.gerar_aposta = lambda *a, **k: None  # type: ignore[assignment]
            return

        # atributos do gerador de números
        self._range = range(
            self.settings["numeros"][0], self.settings["numeros"][1] + 1
        )
        self._min = self.settings["marcar"][0]
        self._max = self.settings["marcar"][1]
        self._padrao = self.settings.get("padrao", self._min)

    def gerar_aposta(self, marcar: int = None) -> Tuple[int, ...]:
        if marcar in (None, 0):
            marcar = self._padrao
        if not (self._min <= marcar <= self._max):
            raise QuantidadeInvalida(self.nome, marcar)
        result = random.sample(self._range, marcar)
        return tuple(sorted(result))

    def consultar(self, concurso: int = 0) -> Dict[str, Any]:
        """Obtém o resultado do sorteio de um concurso.

        Primeiramente, é verificado se o resultado já existe em cache no banco de dados.
        Caso negativo, faz o download e armazena para uso futuro.
        """
        result = self._cache(concurso)
        if result:
            return result

        result = self._download(concurso)
        self._store(result)

        return result

    def _cache(self, concurso: int) -> Dict[str, Any]:
        result = self.loteria_db.get("%s|%s" % (self.nome, concurso))
        if result:
            # convert `(k, v)` de volta para `dict`
            _result = json.loads(result)
            _result["premios"] = collections.OrderedDict(_result["premios"])

            return _result

        return None

    def _download(self, concurso: int) -> Dict[str, Any]:
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

    def _store(self, result: Dict[str, Any]) -> None:
        # converte `dict` para `(k, v)`: garante os prêmios na ordem devolvida pelo parser
        result = result.copy()
        result["premios"] = list(result["premios"].items())
        # armazena no cache
        self.loteria_db["%s|%s" % (self.nome, result["concurso"])] = json.dumps(result)

    def conferir(self, concurso: int, apostas: List[List[int]]) -> List[Dict[str, Any]]:
        result = self.consultar(concurso)
        resp = []
        for aposta in apostas:
            if self._kind == K_COMMON:
                acertou = [[n for n in res if n in aposta] for res in result["numeros"]]
            else:
                acertou = [aposta for res in result["premios"] if [res] == aposta]

            ganhou = self._ganhou(result, acertou)
            resp.append(
                {
                    "concurso": result["concurso"],
                    "numeros": aposta,
                    "acertou": acertou,
                    "ganhou": ganhou,
                }
            )
        return resp

    def _ganhou(self, result: Dict[str, Any], acertou: List[List[int]]) -> List[str]:
        if self._kind == K_COMMON:
            marcou = [len(t) for t in acertou]
            if self.nome == "duplasena" and marcou[0] == 6:
                marcou[0] = -6
        else:
            marcou = [v for [v] in acertou] or [None]

        return [result["premios"].get(n, "0,00") for n in marcou]

    def _url(
        self,
        concurso: int,
        base: str = "http://www1.caixa.gov.br/loterias/loterias/%(loteria)s/",
        script: str = "%(loteria)s_pesquisa_new.asp",
        query: str = "?submeteu=sim&opcao=concurso&txtConcurso=%(concurso)d",
    ) -> str:
        script = self.settings.get("url-script", script)
        if concurso <= 0:
            return (base + script) % {"loteria": self.nome}
        else:
            return (base + script + query) % {
                "loteria": self.nome,
                "concurso": concurso,
            }


class LoteriaParser:
    NEW = 1
    SPECS = {
        "quina": {
            "numeros": [(21, 25)],
            "premios": {
                5: 7,
                4: 9,
                3: 11,
            },
            "parser": NEW,
        },
        "megasena": {
            "numeros": [(28, 33)],
            "premios": {
                6: 11,
                5: 13,
                4: 15,
            },
            "parser": NEW,
        },
        "lotofacil": {
            "numeros": [(3, 17)],
            "premios": {
                15: 19,
                14: 21,
                13: 23,
                12: 25,
                11: 27,
            },
        },
        "lotomania": {
            "numeros": [(6, 25)],
            "premios": {
                20: 28,
                19: 30,
                18: 32,
                17: 34,
                16: 36,
                0: 38,
            },
        },
        "duplasena": {
            "numeros": [(4, 9), (12, 17)],
            "premios": {
                -6: 21,
                6: 24,
                5: 25,
                4: 27,
            },
            "parser": NEW,
        },
        "federal": {
            "concurso": 2,
            "numeros": (6, 8, 10, 12, 14),
            "premios": (7, 9, 11, 13, 15),
            "kind": K_TICKET,
        },
    }

    def __init__(self, nome: str) -> None:
        self._spec = self.SPECS.get(nome)
        if self._spec is None:
            raise NotImplementedError("parser")
        if "premios" not in self._spec:
            raise NotImplementedError("parser: premios")

        if self._spec.get("parser") == self.NEW:
            self._parser: _Parser = _NewParser()
        else:
            self._parser: _Parser = _OldParser()  # type: ignore[no-redef]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._parser, name)

    def data(self) -> Dict[str, Any]:
        spec = self._spec
        dados = "".join(self._parser.data).split("|")

        kind = spec.get("kind", K_COMMON)
        if kind == K_COMMON:
            subdados = self.__common(spec, dados)
        else:
            subdados = self.__ticket(spec, dados)

        if subdados:
            numeros, premios = subdados
        else:
            return None

        return {
            "concurso": int(dados[spec.get("concurso", 0)]),  # type: ignore[call-overload]
            "numeros": numeros,
            "premios": premios,
        }

    @staticmethod
    def __common(
        spec: Dict[str, Any], dados: List[str]
    ) -> Tuple[List[List[int]], Dict[int, str]]:
        pos_nums = [range(p[0], p[1] + 1) for p in spec["numeros"]]
        try:
            numeros = [[int(dados[i]) for i in r] for r in pos_nums]
            premios = collections.OrderedDict()
            for qnt, pos_premio in sorted(spec["premios"].items(), reverse=True):
                premios[qnt] = dados[pos_premio]

            return numeros, premios
        except (IndexError, ValueError):
            return None

    @staticmethod
    def __ticket(spec: Dict[str, Any], dados: List[str]) -> Tuple[None, Dict[int, str]]:
        try:
            premios = collections.OrderedDict()
            for pos_ticket, pos_premio in zip(spec["numeros"], spec["premios"]):
                ticket = int(dados[pos_ticket].replace(".", ""))
                premios[ticket] = dados[pos_premio]

            return None, premios
        except (IndexError, ValueError):
            return None


class _Parser(HTMLParser, metaclass=ABCMeta):
    @property
    @abstractmethod
    def data(self) -> List[str]:
        ...


class _OldParser(_Parser):
    def __init__(self) -> None:
        super().__init__()
        self._capture: bool
        self._data: List[str]

    @property
    def data(self) -> List[str]:
        return self._data

    def reset(self) -> None:
        super().reset()

        self._capture = True
        self._data = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        self._capture = False

    def handle_endtag(self, tag: str) -> None:
        self._capture = True

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._data.append(data)

    def error(self, message: str) -> None:
        raise RuntimeError(message)


class _NewParser(_OldParser):
    def __init__(self) -> None:
        super().__init__()
        self._capture_list: bool
        self._capture_number: bool
        self._numbers: List[str]

    def reset(self) -> None:
        super().reset()

        self._capture_list = False
        self._capture_number = False
        self._numbers = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        super().handle_starttag(tag, attrs)

        if tag == "ul":
            self._capture_list = True

        elif tag == "li" and self._capture_list:
            self._capture_number = True

    def handle_endtag(self, tag: str) -> None:
        super().handle_endtag(tag)

        if tag == "li" and self._capture_list:
            self._capture_number = False

        elif tag == "ul" and len(self._numbers) > 0:
            self._data.append("|" + "|".join(self._numbers) + "|")
            self._capture_list = False
            self._numbers = []

    def handle_data(self, data: str) -> None:
        super().handle_data(data)

        if self._capture_number:
            self._numbers.append(data)
