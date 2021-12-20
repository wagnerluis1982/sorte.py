from __future__ import annotations

from typing import TypedDict


class ResultadoQuinaDict(TypedDict):
    tipoJogo: str
    numero: int
    nomeMunicipioUFSorteio: str
    dataApuracao: str
    valorArrecadado: float
    valorEstimadoProximoConcurso: float
    valorAcumuladoProximoConcurso: float
    valorAcumuladoConcursoEspecial: float
    valorAcumuladoConcurso_0_5: float
    acumulado: bool
    indicadorConcursoEspecial: int
    dezenasSorteadasOrdemSorteio: list[str]
    listaResultadoEquipeEsportiva: str
    numeroJogo: int
    nomeTimeCoracaoMesSorte: str
    tipoPublicacao: int
    observacao: str
    localSorteio: str
    dataProximoConcurso: str
    numeroConcursoAnterior: int
    numeroConcursoProximo: int
    valorTotalPremioFaixaUm: int
    numeroConcursoFinal_0_5: int
    listaMunicipioUFGanhadores: list[str]
    listaRateioPremio: list[RateioPremioDict]
    listaDezenas: list[str]


class RateioPremioDict(TypedDict):
    faixa: int
    numeroDeGanhadores: int
    valorPremio: float
    descricaoFaixa: str
