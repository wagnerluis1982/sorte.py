import json

from datetime import datetime
from pathlib import Path

from sortepy.v2.loterica.handlers import QuinaResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


def test_quina_handler(fixtures_dir: Path):
    handler = QuinaResponseHandler()
    data = json.load(open(fixtures_dir / "response_quina_5734.json"))

    actual_result = handler.handle(data)

    assert actual_result == DrawResult(
        draw_date=datetime(year=2021, month=12, day=18),
        draw_number="5734",
        draw_details=[
            DrawDetail(
                ball_numbers=[26, 27, 29, 74, 77],
                jackpot=10_358_517.22,
                currency="BRL",
                prize_breakdown={
                    "5": DrawPrize(winners=0, prize=0.00),
                    "4": DrawPrize(winners=61, prize=8093.88),
                    "3": DrawPrize(winners=6120, prize=76.83),
                    "2": DrawPrize(winners=151744, prize=3.09),
                },
            )
        ],
    )
