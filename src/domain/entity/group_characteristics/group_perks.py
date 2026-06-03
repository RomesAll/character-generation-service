import copy
import weakref
from dataclasses import dataclass, field
from typing import NewType, Literal

from src.domain.exceptions import DuplicatePerkException, NotFoundPerkException
from src.domain.value_object.enums import Measurement, StatEnum
from src.domain.value_object.perk import Perk, PerkMultiplier
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.characters import Character
    from src.domain.entity.stats import BaseStat

NamePerk = NewType("NamePerk", str)
AmountPerk = NewType("AmountPerk", int)


@dataclass
class GroupPerk:
    _perks: list[Perk] = field(default_factory=list)
    _character: weakref.ref['Character'] | None = field(default=None, init=False)

    @property
    def perks(self) -> list[Perk]:
        return copy.deepcopy(self._perks)

    def get_copy(self) -> 'GroupPerk':
        return copy.deepcopy(self)

    def add(
        self, name: NamePerk, stats: list[tuple[StatEnum, AmountPerk, Measurement]]
    ):
        for perk in self._perks:
            if perk.name == name:
                raise DuplicatePerkException(name)
        perk: Perk = Perk(name=name)
        for stat, amount, measurement in stats:
            perk.multipliers.append(PerkMultiplier(
                owner=weakref.ref(perk),
                stat=stat,
                amount=amount,
                measurement=measurement
            ))
        self._perks.append(perk)
        if self._character:
            for multiplier in perk.multipliers:
                self._character().stats.append_multipliers(multiplier)
        return self

    def remove(self, name: NamePerk):
        for perk in self._perks:
            if perk.name == name:
                if self._character:
                    for multiplier in perk.multipliers:
                        self._character().stats.remove_multipliers(multiplier)
                self._perks.remove(perk)
                return self
        raise NotFoundPerkException(name)

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

    def add_all_multiplier(self):
        for perk in self._perks:
            self.add_multiplier(perk=perk)

    def add_multiplier(self, perk: Perk):
        for multiplier in perk.multipliers:
            if self._character:
                stat_obj: 'BaseStat' = self._character().stats.get_stat(multiplier.stat)
                stat_obj.append_multipliers(multiplier)