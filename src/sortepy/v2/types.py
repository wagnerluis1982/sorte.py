from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Mapping
from typing import Sequence
from typing import Union


if TYPE_CHECKING:
    from datetime import datetime


# TODO: remove ignore[call-overload] comments when mypy hook supports py3.10 (due to `kw_only`)


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawPrize:
    winners: int
    prize: int | float
    context: Mapping[str, Any] | None = None


_PrizesAsMapping = Mapping[str, DrawPrize]
_PrizesAsSequence = Sequence[DrawPrize]
PrizeBreakdown = Union[_PrizesAsMapping, _PrizesAsSequence]


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawDetail:
    ball_numbers: Sequence[int]
    jackpot: int | float
    currency: str
    prize_breakdown: PrizeBreakdown


@dataclass(frozen=True, kw_only=True)  # type: ignore[call-overload]
class DrawResult:
    draw_date: datetime
    draw_number: str
    draw_details: Sequence[DrawDetail]
