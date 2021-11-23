from typing import Dict
from typing import List
from typing import TypedDict


class ResultadoDict(TypedDict):
    concurso: int
    numeros: List[List[int]]
    premios: Dict[int, str]


class ConferenciaDict(TypedDict):
    concurso: int
    numeros: List[int]
    acertou: List[List[int]]
    ganhou: List[str]
