from typing import Callable, TYPE_CHECKING
from src.domain.value_object import BodyPart

if TYPE_CHECKING:
    from src.domain.entity.fast_slot.armor_fast_slot import ArmorFastSlot
    from src.domain.entity.fast_slot.arms_fast_slot import ArmsFastSlot
    from src.domain.entity.group_characteristics import GroupStat
    from src.domain.entity.outfits import Armor, Arms


def change_armor_stats(func: Callable) -> Callable:
    def wrapper(
        self: "ArmorFastSlot.ManageArmorItem", *, item: "Armor | None" = None
    ) -> "Armor | None":
        group_stat: "GroupStat" = self.outer().group_stat
        if not group_stat:
            return func(self, item=item)
        if self.body_part_name == BodyPart.HEAD:
            group_stat.with_head_armor(
                current=item.current_durability if item else 0,
                maximum=item.max_durability if item else 0,
            )
        elif self.body_part_name == BodyPart.BODY:
            group_stat.with_body_armor(
                current=item.current_durability if item else 0,
                maximum=item.max_durability if item else 0,
            )
        return func(self, item=item)

    return wrapper


def change_damage_stats(func: Callable) -> Callable:
    def wrapper(
        self: "ArmsFastSlot.ManageHandItem", *, item: "Arms | None" = None
    ) -> "Arms | None":
        group_stat: "GroupStat" = self.outer().group_stat
        if not group_stat:
            return func(self, item=item)
        group_stat.with_damage(
            current=item.damage if item else (0, 0),
            maximum=item.damage[1] if item else 0,
        )
        old_item = func(self, item=item)
        return old_item

    return wrapper