import weakref
from dataclasses import dataclass, field

from src.domain.entity.stats.base import BaseStat
from src.domain.value_object.enums import Measurement
from src.domain.entity.stats import StatEnum
from typing import NewType, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.stats import MultiplierObject
    from src.domain.entity.characters.character import Character

NamePerk = NewType('NamePerk', str)
AmountPerk = NewType('AmountPerk', int)

@dataclass(frozen=True)
class PerkStat:
    stat: StatEnum
    amount: int
    measurement: Measurement

@dataclass(frozen=True)
class Perk:
    name: str
    stats: list[PerkStat] = field(default_factory=list)

class GroupPerk:
    def __init__(self):
        self.perks = []
        self.character: weakref.ref[Character] | None = None

    def add(self, name: NamePerk, stats: list[tuple[StatEnum, AmountPerk, Measurement]]):
        perk = Perk(name=name)
        for stat, amount, measurement in stats:
            perk.stats.append(PerkStat(stat, amount, measurement))
            if self.character:
                character_stat: BaseStat = self.character().stats.get_stat(stat)
                multiplier: MultiplierObject = (amount, measurement)
                character_stat.append_multipliers(multiplier)
        self.perks.append(perk)
        return self

    def remove(self, name: NamePerk):
        for perk in self.perks:
            if perk.name == name:
                self.perks.remove(perk)
                return self
        raise ValueError(f'Perk {name} not found')