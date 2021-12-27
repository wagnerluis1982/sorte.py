from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar


T = TypeVar("T")

if TYPE_CHECKING:
    from sortepy.v2.types import DrawResult


class DrawResponseHandler(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def handle(self, data: T) -> DrawResult:
        """Handles a response data and gives a structured result.

        >>> h.handle(data)
        DrawResult(
            draw_date=datetime.datetime(2021, 12, 4, 0, 0),
            draw_number="5722",
            draw_details=[
                DrawDetail(
                    ball_numbers=[14, 40, 51, 56, 57],
                    jackpot=4_700_000,
                    currency="BRL",
                    prize_breakdown={
                        "5": DrawPrize(winners=0, prize=0),
                        "4": DrawPrize(winners=50, prize=9043.15),
                        "3": DrawPrize(winners=4_254, prize=101.22),
                        "2": DrawPrize(winners=117_464, prize=3.66)
                    }
                )
            ]
        )
        """
