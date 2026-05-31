from dataclasses import dataclass, field
from typing import NewType

from src.domain.value_object.enums import Measurement, StatEnum
from src.domain.value_object.perk import Perk, PerkMultiplier

NamePerk = NewType("NamePerk", str)
AmountPerk = NewType("AmountPerk", int)


@dataclass
class GroupPerk:
    _perks: list[Perk] = field(default_factory=list)

    @property
    def perks(self) -> list[Perk]:
        return self._perks

    def add(
        self, name: NamePerk, stats: list[tuple[StatEnum, AmountPerk, Measurement]]
    ):
        perk = Perk(name=name)
        for stat, amount, measurement in stats:
            perk.stats.append(PerkMultiplier(stat, amount, measurement))
        self._perks.append(perk)
        return self

    def remove(self, name: NamePerk):
        for perk in self._perks:
            if perk.name == name:
                self._perks.remove(perk)
                return self
        raise ValueError(f"Perk {name} not found")
