import json

from datetime import datetime
from pathlib import Path

from sortepy.v2.loterica.handlers import FederalResponseHandler
from sortepy.v2.loterica.handlers import LotofacilResponseHandler
from sortepy.v2.loterica.handlers import QuinaResponseHandler
from sortepy.v2.types import DrawPrize


def test_federal_handler(fixtures_dir: Path):
    handler = FederalResponseHandler()
    data = json.load(open(fixtures_dir / "response_federal_5624.json"))

    result = handler.handle(data)
    assert result.draw_date == datetime(year=2021, month=12, day=22)
    assert result.draw_number == "5624"
    assert len(result.draw_details) == 1

    draw = result.draw_details[0]
    assert draw.ball_numbers == [86447, 26701, 28242, 3477, 66757]
    assert draw.jackpot == 0.00
    assert draw.currency == "BRL"
    assert draw.prize_breakdown == (
        DrawPrize(winners=1, prize=500_000.00, context={"ticket": "086447"}),
        DrawPrize(winners=1, prize=27_000.00, context={"ticket": "026701"}),
        DrawPrize(winners=1, prize=24_000.00, context={"ticket": "028242"}),
        DrawPrize(winners=1, prize=19_000.00, context={"ticket": "003477"}),
        DrawPrize(winners=1, prize=18_329.00, context={"ticket": "066757"}),
    )


def test_lotofacil_handler(fixtures_dir: Path):
    handler = LotofacilResponseHandler()
    data = json.load(open(fixtures_dir / "response_lotofacil_2402.json"))

    result = handler.handle(data)
    assert result.draw_date == datetime(year=2021, month=12, day=20)
    assert result.draw_number == "2402"
    assert len(result.draw_details) == 1

    draw = result.draw_details[0]
    assert draw.ball_numbers == [1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 18, 20, 23, 25]
    assert draw.jackpot == 0.00
    assert draw.currency == "BRL"
    assert draw.prize_breakdown == (
        DrawPrize(hits=15, winners=3, prize=370_337.82),
        DrawPrize(hits=14, winners=321, prize=1036.73),
        DrawPrize(hits=13, winners=13_409, prize=25.00),
        DrawPrize(hits=12, winners=144_941, prize=10.00),
        DrawPrize(hits=11, winners=741_668, prize=5.00),
    )


def test_quina_handler(fixtures_dir: Path):
    handler = QuinaResponseHandler()
    data = json.load(open(fixtures_dir / "response_quina_5734.json"))

    result = handler.handle(data)
    assert result.draw_date == datetime(year=2021, month=12, day=18)
    assert result.draw_number == "5734"
    assert len(result.draw_details) == 1

    draw = result.draw_details[0]
    assert draw.ball_numbers == [26, 27, 29, 74, 77]
    assert draw.jackpot == 10_358_517.22
    assert draw.currency == "BRL"
    assert draw.prize_breakdown == (
        DrawPrize(hits=5, winners=0, prize=0.00),
        DrawPrize(hits=4, winners=61, prize=8093.88),
        DrawPrize(hits=3, winners=6120, prize=76.83),
        DrawPrize(hits=2, winners=151744, prize=3.09),
    )
