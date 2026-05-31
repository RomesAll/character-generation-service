from dataclasses import dataclass, field
from src.domain.value_object.enums import Measurement, StatEnum
from typing import NewType

NamePerk = NewType("NamePerk", str)
AmountPerk = NewType("AmountPerk", int)


@dataclass(frozen=True)
class PerkMultiplier:
    stat: StatEnum
    amount: int
    measurement: Measurement


@dataclass(frozen=True)
class Perk:
    name: str
    stats: list[PerkMultiplier] = field(default_factory=list)
