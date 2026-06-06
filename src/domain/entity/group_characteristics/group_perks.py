from dataclasses import dataclass, field
from typing import Self
import copy, weakref

from src.domain.entity.group_characteristics.decorators import (
    check_duplicate_perk,
    add_multiplier_in_character,
    check_existing_perk,
    remove_multiplier_in_character,
)
from src.domain.entity.group_characteristics.group_stats import GroupStat
from src.domain.entity.stats import BaseStat
from src.domain.exceptions import GroupStatsRefNotFoundException, DuplicateMultiplierException
from src.domain.value_object.perk import Perk, PerkMultiplier


@dataclass
class GroupPerk:
    _perks: list[Perk] = field(default_factory=list, init=False)
    _group_stats_ref: weakref.ref["GroupStat"] | None = field(
        default=None, compare=False, repr=False, init=False
    )

    def __init__(self, group_stats: weakref.ref["GroupStat"] | None = None) -> None:
        super().__init__()
        self._group_stats_ref = group_stats
        self._perks = []

    @property
    def perks(self) -> list[Perk]:
        return copy.deepcopy(self._perks)

    @property
    def group_stats(self):
        return self._group_stats_ref() if self._group_stats_ref else None

    @group_stats.setter
    def group_stats(self, value: weakref.ref["GroupStat"]):
        self._group_stats_ref = value

    def get_copy(self) -> "GroupPerk":
        return copy.deepcopy(self)

    @check_duplicate_perk
    @add_multiplier_in_character
    def add(self, *, name_perk: str, multipliers: list[PerkMultiplier]) -> Self:
        new_perk = Perk(name_perk, multipliers=tuple(multipliers))
        self._perks.append(new_perk)
        return self

    @check_existing_perk
    @remove_multiplier_in_character
    def remove(self, *, name_perk: str, **kwargs) -> Self:
        perk_ind: int = kwargs.get("perk_ind")
        self._perks.pop(perk_ind)
        return self

    @check_existing_perk
    def get_perk_by_name(self, *, name_perk: str, **kwargs) -> Perk:
        perk_ind: int = kwargs.get("perk_ind")
        return self._perks[perk_ind]

    def refresh_all_multiplier(self):
        if not self.group_stats:
            raise GroupStatsRefNotFoundException()
        for perk in self._perks:
            for multiplier in perk.multipliers:
                try:
                    stat: BaseStat = getattr(self.group_stats, multiplier.stat.value)
                    stat.append_multipliers(multiplier)
                except DuplicateMultiplierException:
                    continue