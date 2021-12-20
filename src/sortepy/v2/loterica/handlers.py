from __future__ import annotations

from datetime import datetime

from sortepy.v2.loterica._types import ResultadoT1Dict
from sortepy.v2.spi import DrawResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


class LotofacilResponseHandler(DrawResponseHandler[ResultadoT1Dict]):
    def handle(self, data: ResultadoT1Dict) -> DrawResult:
        hit_mapping = {
            "15 acertos": "15",
            "14 acertos": "14",
            "13 acertos": "13",
            "12 acertos": "12",
            "11 acertos": "11",
        }
        return _handle_response_type1(data, hit_mapping)


class QuinaResponseHandler(DrawResponseHandler[ResultadoT1Dict]):
    def handle(self, data: ResultadoT1Dict) -> DrawResult:
        hit_mapping = {
            "5 acertos": "5",
            "4 acertos": "4",
            "3 acertos": "3",
            "2 acertos": "2",
        }
        return _handle_response_type1(data, hit_mapping)


def _handle_response_type1(data: ResultadoT1Dict, hit_mapping: dict) -> DrawResult:
    return DrawResult(
        draw_date=datetime.strptime(data["dataApuracao"], "%d/%m/%Y"),
        draw_number=str(data["numero"]),
        draw_details=[
            DrawDetail(
                ball_numbers=[int(n) for n in data["listaDezenas"]],
                jackpot=data["valorAcumuladoProximoConcurso"],
                currency="BRL",
                prize_breakdown=_get_prizes_type1(data, hit_mapping),
            )
        ],
    )


def _get_prizes_type1(data: ResultadoT1Dict, hit_mapping: dict) -> dict[str, DrawPrize]:
    prizes = {}
    for p in data["listaRateioPremio"]:
        key = hit_mapping[p["descricaoFaixa"]]
        value = DrawPrize(winners=p["numeroDeGanhadores"], prize=p["valorPremio"])
        prizes[key] = value

    return prizes
