from typing import Dict
from typing import List
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
