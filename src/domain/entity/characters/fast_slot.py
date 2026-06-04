import copy
import weakref

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

from src.domain.entity.outfits import MeleeArms
from src.domain.entity.stats import Damage, BaseStat
from src.domain.exceptions import BodyPartArmorException
from src.domain.value_object.enums import EquipmentType, BodyPart, StatEnum
from src.domain.entity.outfits.arms import Equipment
from src.domain.entity.outfits.armor import Armor, HeadArmor, BodyArmor

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.domain.entity.characters.character import Character

def change_damage_stat(func: Callable) -> Callable:
    def wrapper(self: 'ArmsFastSlot.ManageHandItem', *args, **kwargs):
        result: None | Equipment | MeleeArms  = func(self, *args, **kwargs)
        character = self.outer().get_character()()
        current_damage_stat: BaseStat = character.stats.get_stat(StatEnum.DAMAGE)
        if type(result) is MeleeArms:
            current_damage_stat.current -= result.damage
            current_damage_stat.maximum -= result.damage
        if type(args[0]) is MeleeArms:
            current_damage_stat.current += args[0].damage
            current_damage_stat.maximum += args[0].damage
        return result
    return wrapper

class ArmsFastSlot(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    left_hand: "ArmsFastSlot.ManageHandItem | None" = Field(
        None, description="Слот под левую руку"
    )
    right_hand: "ArmsFastSlot.ManageHandItem | None" = Field(
        None, description="Слот под правую руку"
    )
    _character: weakref.ref['Character'] | None = PrivateAttr(None)

    def __init__(
        self,
        character: weakref.ref['Character'] | None = None,
        left_hand: Equipment | None = None,
        right_hand: Equipment | None = None,
    ):
        super().__init__()
        self._character = character
        self.left_hand = self.ManageHandItem(
            hand_name=BodyPart.LEFT_HAND, item_in_hand=left_hand, outer=weakref.ref(self)
        )
        self.right_hand = self.ManageHandItem(
            hand_name=BodyPart.RIGHT_HAND, item_in_hand=right_hand, outer=weakref.ref(self)
        )
        self.left_hand.other_hand = self.right_hand
        self.right_hand.other_hand = self.left_hand

    def get_copy(self) -> "ArmsFastSlot":
        return copy.deepcopy(self)

    def get_character(self) -> "weakref.ref[Character]":
        return self._character

    class ManageHandItem(BaseModel):
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

        hand_name: BodyPart
        item_in_hand: Equipment | None = None
        other_hand: "ArmsFastSlot.ManageHandItem | None" = Field(None, repr=False)
        outer: weakref.ref['ArmsFastSlot']

        @change_damage_stat
        def equip(
            self, item: Equipment | None = None
        ) -> Equipment | tuple[Equipment, ...] | tuple[None, ...] | None:
            old_item_self: Equipment = self.item_in_hand
            old_item_other: Equipment = self.other_hand.item_in_hand
            if item and item.type_equipment == EquipmentType.TWO_HAND:
                self.item_in_hand = item
                self.other_hand.item_in_hand = item
                if id(old_item_self) != id(old_item_other):
                    return old_item_self, old_item_other
                return old_item_self
            if old_item_self and old_item_self.type_equipment == EquipmentType.TWO_HAND:
                self.other_hand.item_in_hand = None
            self.item_in_hand = item
            return old_item_self

        def unequip(
            self,
        ) -> Equipment | tuple[Equipment, ...] | tuple[None, ...] | None:
            return self.equip(None)


class ArmorFastSlot(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    head: "ArmorFastSlot.ManageArmorItem | None" = Field(
        None, description="Слот для головы"
    )
    body: "ArmorFastSlot.ManageArmorItem | None" = Field(
        None, description="Слот для тела"
    )
    _character: weakref.ref['Character'] | None = PrivateAttr(None)

    def __init__(
        self,
        character: weakref.ref['Character'] | None = None,
        head: HeadArmor | None = None,
        body: BodyArmor | None = None,
    ):
        super().__init__()
        self._character = character
        self.head = self.ManageArmorItem(body_part_name=BodyPart.HEAD, armor=head, outer=weakref.ref(self))
        self.body = self.ManageArmorItem(body_part_name=BodyPart.BODY, armor=body, outer=weakref.ref(self))

    def get_copy(self) -> "ArmorFastSlot":
        return copy.deepcopy(self)

    class ManageArmorItem(BaseModel):
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

        body_part_name: BodyPart
        armor: Armor | HeadArmor | BodyArmor | None = None
        outer: weakref.ref['ArmorFastSlot']

        def equip(self, new_armor: Armor | None = None) -> Armor | None:
            if new_armor and self.body_part_name != new_armor.body_part:
                raise BodyPartArmorException(new_armor, self.body_part_name)
            old_armor = self.armor
            self.armor = new_armor
            return old_armor

        def unequip(self) -> Armor | None:
            return self.equip(None)
