from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Dict
from typing import Sequence


if TYPE_CHECKING:
    from datetime import datetime


# TODO: remove ignore[call-overload] comments when mypy hook supports py3.10 (due to `kw_only`)


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawResult:
    draw_date: datetime
    draw_number: str
    draw_details: Sequence[DrawDetail]


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawDetail:
    ball_numbers: Sequence[int]
    jackpot: int | float
    currency: str
    prize_breakdown: Dict[str, DrawPrize]


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawPrize:
    winners: int
    prize: int | float
