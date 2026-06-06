from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.fast_slot.armor_fast_slot import ArmorFastSlot
    from src.domain.entity.fast_slot.arms_fast_slot import ArmsFastSlot
    from src.domain.entity.group_characteristics import GroupStat
    from src.domain.entity.outfits import Armor, Arms
    from src.domain.value_object import BodyPart


def change_armor_stats(func: Callable) -> Callable:
    def wrapper(
        self: "ArmorFastSlot.ManageArmorItem", *, new_armor: "Armor | None" = None
    ) -> "Armor | None":
        group_stat: "GroupStat" = self.outer().group_stat
        if self.body_part_name == BodyPart.HEAD:
            group_stat.with_head_armor(
                current=new_armor.current_durability if new_armor else 0,
                maximum=new_armor.max_durability if new_armor else 0,
            )
        elif self.body_part_name == BodyPart.BODY:
            group_stat.with_body_armor(
                current=new_armor.current_durability if new_armor else 0,
                maximum=new_armor.max_durability if new_armor else 0,
            )
        old_item = func(self, new_armor=new_armor)
        return old_item

    return wrapper


def change_damage_stats(func: Callable) -> Callable:
    def wrapper(
        self: "ArmsFastSlot.ManageHandItem", *, item: "Arms | None" = None
    ) -> "Arms | None":
        group_stat: "GroupStat" = self.outer().group_stat
        group_stat.with_damage(
            current=item.damage if item else (0, 0),
            maximum=item.damage[1] if item else 0,
        )
        old_item = func(self, item=item)
        return old_item

    return wrapper
