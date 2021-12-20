import json

from datetime import datetime
from pathlib import Path

from sortepy.v2.loterica.handlers import LotofacilResponseHandler
from sortepy.v2.loterica.handlers import QuinaResponseHandler
from sortepy.v2.types import DrawDetail
from sortepy.v2.types import DrawPrize
from sortepy.v2.types import DrawResult


def test_lotofacil_handler(fixtures_dir: Path):
    handler = LotofacilResponseHandler()
    data = json.load(open(fixtures_dir / "response_lotofacil_2402.json"))

    actual_result = handler.handle(data)

    assert actual_result == DrawResult(
        draw_date=datetime(year=2021, month=12, day=20),
        draw_number="2402",
        draw_details=[
            DrawDetail(
                ball_numbers=[1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 18, 20, 23, 25],
                jackpot=0.00,
                currency="BRL",
                prize_breakdown={
                    "15": DrawPrize(winners=3, prize=370_337.82),
                    "14": DrawPrize(winners=321, prize=1036.73),
                    "13": DrawPrize(winners=13_409, prize=25.00),
                    "12": DrawPrize(winners=144_941, prize=10.00),
                    "11": DrawPrize(winners=741_668, prize=5.00),
                },
            )
        ],
    )


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
