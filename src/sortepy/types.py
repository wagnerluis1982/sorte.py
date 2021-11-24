from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypedDict


class Aposta(List[int]):
    pass


class ResultadoDict(TypedDict):
    concurso: int
    numeros: List[Aposta]
    premios: Dict[int, str]


class ConferenciaDict(TypedDict):
    concurso: int
    numeros: Aposta
    acertou: List[Aposta]
    ganhou: List[str]


@dataclass(frozen=True)
class LoteriaConfig:
    marcar: Tuple[int, int] = None
    numeros: Tuple[int, int] = None
    nome: str = None
    padrao: int = None
    url_script: str = None
    kind: int = None
