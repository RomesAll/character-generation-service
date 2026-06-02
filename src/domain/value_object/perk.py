from dataclasses import dataclass, field
from src.domain.value_object.enums import Measurement, StatEnum
import weakref

@dataclass(frozen=True)
class PerkMultiplier:
    owner: weakref.ref['Perk']
    stat: StatEnum
    amount: int
    measurement: Measurement


@dataclass(frozen=True)
class Perk:
    name: str
    multipliers: list[PerkMultiplier] = field(default_factory=list)