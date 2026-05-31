from dataclasses import dataclass, field
from src.domain.value_object.enums import Measurement, StatEnum
from typing import NewType

NamePerk = NewType("NamePerk", str)
AmountPerk = NewType("AmountPerk", int)


@dataclass(frozen=True)
class PerkStat:
    stat: StatEnum
    amount: int
    measurement: Measurement


@dataclass(frozen=True)
class Perk:
    name: str
    stats: list[PerkStat] = field(default_factory=list)
