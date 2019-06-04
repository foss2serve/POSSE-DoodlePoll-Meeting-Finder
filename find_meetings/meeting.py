from typing import FrozenSet
from dataclasses import dataclass


@dataclass
class Meeting:
    weekday: int
    hour: int
    facilitators: FrozenSet[str] = frozenset()
    participants: FrozenSet[str] = frozenset()
