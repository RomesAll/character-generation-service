from typing import Callable, TYPE_CHECKING
from src.domain.entity.outfits import (
    MeleeArms,
    ShieldArms,
    HeadArmor,
    BodyArmor,
)

if TYPE_CHECKING:
    from src.domain.entity.group_characteristics import GroupStat


def change_head_armor_stats(group_stat: "GroupStat", item: "HeadArmor | None"):
    group_stat.with_head_armor(
        current=item.current_durability if item else 0,
        maximum=item.max_durability if item else 0,
    )


def change_body_armor_stats(group_stat: "GroupStat", item: "BodyArmor | None"):
    group_stat.with_body_armor(
        current=item.current_durability if item else 0,
        maximum=item.max_durability if item else 0,
    )


def change_melee_arms_stats(group_stat: "GroupStat", item: "MeleeArms | None"):
    group_stat.with_damage(
        current=item.damage if item else (0, 0),
        maximum=item.damage[1] if item else 0,
    )
    group_stat.with_damage_armor(
        current=item.damage_armor if item else 0,
        maximum=item.damage_armor if item else 0,
    )


def change_shield_stats(group_stat: "GroupStat", item: "ShieldArms | None"):
    group_stat.with_melee_defense(
        current=item.melee_defense if item else 0,
        maximum=item.melee_defense if item else 0,
    )
    group_stat.with_shooting_skill(
        current=item.shooting_protection if item else 0,
        maximum=item.shooting_protection if item else 0,
    )


MAPPING_OUTFITS_STATS = {
    MeleeArms: change_melee_arms_stats,
    ShieldArms: change_shield_stats,
    HeadArmor: change_head_armor_stats,
    BodyArmor: change_body_armor_stats,
}


def change_character_stats(func: Callable) -> Callable:
    def wrapper(self, *, item=None):
        group_stat: "GroupStat" = self.outer().group_stat
        old_item = func(self, item=item)
        if group_stat and item:
            MAPPING_OUTFITS_STATS.get(type(item))(group_stat=group_stat, item=item)
        else:
            MAPPING_OUTFITS_STATS.get(type(old_item))(group_stat=group_stat, item=None)
        return old_item

    return wrapper
