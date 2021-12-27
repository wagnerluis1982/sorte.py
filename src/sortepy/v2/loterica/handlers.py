from __future__ import annotations

from datetime import datetime
from typing import Iterator
from typing import Sequence

from sortepy.v2.loterica._types import LotericaResponseDict
from sortepy.v2.spi import DrawResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


class FederalResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        federal_prizes = self._iter_federal_prizes(data)
        return _handle_response_type1(data, tuple(federal_prizes))

    @staticmethod
    def _iter_federal_prizes(data: LotericaResponseDict) -> Iterator[DrawPrize]:
        tickets = data["listaDezenas"]
        raw_prizes = data["listaRateioPremio"]
        for i, v in enumerate(raw_prizes):
            yield DrawPrize(
                winners=v["numeroDeGanhadores"],
                prize=v["valorPremio"],
                context={"ticket": tickets[i]},
            )


class LotofacilResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        return _handle_response_type1(data)


class QuinaResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        return _handle_response_type1(data)


def _handle_response_type1(
    data: LotericaResponseDict, prize_breakdown: Sequence[DrawPrize] = None
) -> DrawResult:
    if prize_breakdown is None:
        prize_breakdown = tuple(_iter_prizes_type1(data))

    return DrawResult(
        draw_date=datetime.strptime(data["dataApuracao"], "%d/%m/%Y"),
        draw_number=str(data["numero"]),
        draw_details=[
            DrawDetail(
                ball_numbers=[int(n) for n in data["listaDezenas"]],
                jackpot=data["valorAcumuladoProximoConcurso"],
                currency="BRL",
                prize_breakdown=prize_breakdown,
            )
        ],
    )


def _iter_prizes_type1(data: LotericaResponseDict) -> Iterator[DrawPrize]:
    raw_prizes = data["listaRateioPremio"]
    for v in raw_prizes:
        hits: str = v["descricaoFaixa"].split()[0]
        yield DrawPrize(
            hits=int(hits),
            winners=v["numeroDeGanhadores"],
            prize=v["valorPremio"],
        )
