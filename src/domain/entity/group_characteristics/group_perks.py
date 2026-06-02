import weakref
from dataclasses import dataclass, field
from typing import NewType, Literal

from src.domain.value_object.enums import Measurement, StatEnum
from src.domain.value_object.perk import Perk, PerkMultiplier

NamePerk = NewType("NamePerk", str)
AmountPerk = NewType("AmountPerk", int)


@dataclass
class GroupPerk:
    _perks: list[Perk] = field(default_factory=list)

    @property
    def perks(self) -> list[Perk]:
        return self._perks.copy()

    def add(
        self, name: NamePerk, stats: list[tuple[StatEnum, AmountPerk, Measurement]]
    ):
        for perk in self._perks:
            if perk.name == name:
                raise ValueError('Duplicate perk name')
        perk: Perk = Perk(name=name)
        for stat, amount, measurement in stats:
            perk.multipliers.append(PerkMultiplier(
                owner=weakref.ref(perk),
                stat=stat,
                amount=amount,
                measurement=measurement
            ))
        self._perks.append(perk)
        return self

    def remove(self, name: NamePerk):
        for perk in self._perks:
            if perk.name == name:
                self._perks.remove(perk)
                return self
        raise ValueError(f"Perk {name} not found")

    def get_perk_by_name(self,
                         name: NamePerk,
                         direction: Literal['left', 'right'] = 'left',
                         default: int | None = -1) -> Perk | None:
        _direction = self._perks
        if direction == 'right':
            _direction = self._perks[::-1]
        for perk in _direction:
            if perk.name == name:
                return perk
        if default is None:
            return None
        raise ValueError('No perk found')