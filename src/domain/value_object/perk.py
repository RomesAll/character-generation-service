from dataclasses import dataclass, field
from src.domain.value_object.enums import StatEnum, Measurement

@dataclass(frozen=True)
class PerkStat:
    stat: StatEnum
    amount: int
    measurement: Measurement

@dataclass(frozen=True)
class Perk:
    name: str
    stats: list[PerkStat] = field(default_factory=list)
