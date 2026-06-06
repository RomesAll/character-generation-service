from typing import Callable
from typing import TYPE_CHECKING

from src.domain.entity.group_characteristics.group_stats import GroupStat
from src.domain.exceptions import DuplicatePerkException, NotFoundPerkException
from src.domain.value_object.perk import PerkMultiplier

if TYPE_CHECKING:
    from src.domain.entity.group_characteristics import GroupPerk

def check_duplicate_perk(func: Callable) -> Callable:
    def wrapper(self: 'GroupPerk', *,
                name_perk: str,
                multipliers: list['PerkMultiplier']) -> 'GroupPerk':
        for perk in self.perks:
            if perk.name == name_perk:
                raise DuplicatePerkException(name_perk)
        result: 'GroupPerk' = func(self, name_perk=name_perk, multipliers=multipliers)
        return result
    return wrapper

def check_existing_perk(func: Callable) -> Callable:
    def wrapper(self: 'GroupPerk', *,
                name_perk: str) -> 'GroupPerk':
        for ind, perk in enumerate(self.perks, 0):
            if perk.name == name_perk:
                result: 'GroupPerk' = func(self, name_perk=name_perk, perk_ind=ind)
                return result
        raise NotFoundPerkException(name_perk)
    return wrapper

def add_multiplier_in_character(func: Callable) -> Callable:
    def wrapper(self: 'GroupPerk', *,
                name_perk: str,
                multipliers: list['PerkMultiplier']) -> 'GroupPerk':
        result: 'GroupPerk' = func(self, name_perk=name_perk, multipliers=multipliers)
        group_stats: GroupStat | None = self.group_stats
        if group_stats:
            for multiplier in multipliers:
                group_stats.append_multipliers(multiplier)
        return result
    return wrapper

def remove_multiplier_in_character(func: Callable) -> Callable:
    def wrapper(self: 'GroupPerk', *,
                name_perk: str,
                perk_ind: int) -> 'GroupPerk':
        group_stats: GroupStat | None = self.group_stats
        delete_perk = self.perks[perk_ind]
        if group_stats:
            for multiplier in delete_perk.multipliers:
                group_stats.remove_multipliers(multiplier)
        result: 'GroupPerk' = func(self, name_perk=name_perk, perk_ind=perk_ind)
        return result
    return wrapper