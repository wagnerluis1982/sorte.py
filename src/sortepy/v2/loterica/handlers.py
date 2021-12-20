from __future__ import annotations

from datetime import datetime

from sortepy.v2.loterica._types import ResultadoQuinaDict
from sortepy.v2.spi import DrawResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


class QuinaResponseHandler(DrawResponseHandler[ResultadoQuinaDict]):
    def handle(self, data: ResultadoQuinaDict) -> DrawResult:
        return DrawResult(
            draw_date=datetime.strptime(data["dataApuracao"], "%d/%m/%Y"),
            draw_number=str(data["numero"]),
            draw_details=[
                DrawDetail(
                    ball_numbers=[int(n) for n in data["listaDezenas"]],
                    jackpot=data["valorAcumuladoProximoConcurso"],
                    currency="BRL",
                    prize_breakdown=self.get_prizes(data),
                )
            ],
        )

    def get_prizes(self, data: ResultadoQuinaDict) -> dict[str, DrawPrize]:
        hit_mapping = {
            "5 acertos": "5",
            "4 acertos": "4",
            "3 acertos": "3",
            "2 acertos": "2",
        }

        prizes = {}
        for p in data["listaRateioPremio"]:
            key = hit_mapping[p["descricaoFaixa"]]
            value = DrawPrize(winners=p["numeroDeGanhadores"], prize=p["valorPremio"])
            prizes[key] = value

        return prizes
