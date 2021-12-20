from __future__ import annotations

from datetime import datetime

from sortepy.v2.loterica._types import LotericaResponseDict
from sortepy.v2.spi import DrawResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


class FederalResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        return _handle_response_type1(data)


class LotofacilResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        return _handle_response_type1(data)


class QuinaResponseHandler(DrawResponseHandler[LotericaResponseDict]):
    def handle(self, data: LotericaResponseDict) -> DrawResult:
        return _handle_response_type1(data)


def _handle_response_type1(data: LotericaResponseDict) -> DrawResult:
    return DrawResult(
        draw_date=datetime.strptime(data["dataApuracao"], "%d/%m/%Y"),
        draw_number=str(data["numero"]),
        draw_details=[
            DrawDetail(
                ball_numbers=[int(n) for n in data["listaDezenas"]],
                jackpot=data["valorAcumuladoProximoConcurso"],
                currency="BRL",
                prize_breakdown=_get_prizes_type1(data),
            )
        ],
    )


def _get_prizes_type1(data: LotericaResponseDict) -> dict[str, DrawPrize]:
    prizes = {}
    for p in data["listaRateioPremio"]:
        key = p["descricaoFaixa"].split()[0]
        value = DrawPrize(winners=p["numeroDeGanhadores"], prize=p["valorPremio"])
        prizes[key] = value

    return prizes
