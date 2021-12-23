from __future__ import annotations

from datetime import datetime
from typing import Iterator

from sortepy.v2.loterica._types import LotericaResponseDict
from sortepy.v2.spi import DrawResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult
from sortepy.v2.types import PrizeBreakdown


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
    data: LotericaResponseDict, prize_breakdown: PrizeBreakdown = None
) -> DrawResult:
    if prize_breakdown is None:
        prize_breakdown = _get_prizes_type1(data)

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


def _get_prizes_type1(data: LotericaResponseDict) -> PrizeBreakdown:
    prizes = {}
    for p in data["listaRateioPremio"]:
        key = p["descricaoFaixa"].split()[0]
        value = DrawPrize(winners=p["numeroDeGanhadores"], prize=p["valorPremio"])
        prizes[key] = value

    return prizes
