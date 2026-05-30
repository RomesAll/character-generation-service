
import weakref
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, ConfigDict

from src.domain.value_object.enums import EquipmentType, BodyPart
from src.domain.entity.outfits.arms import Equipment
from src.domain.entity.outfits.armor import Armor, HeadArmor, BodyArmor


class ArmsFastSlot(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )

    left_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, description='Слот под левую руку')
    right_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, description='Слот под правую руку')
    character: weakref.ref | None = Field(None)

    def __init__(self,
                 left_hand: Equipment | None = None,
                 right_hand: Equipment| None = None,
                 character: weakref.ref | None = None,):
        super().__init__()
        self.left_hand = self.ManageHandItem(
            hand_name=BodyPart.LEFT_HAND,
            item_in_hand=left_hand,
            character=character
        )
        self.right_hand = self.ManageHandItem(
            hand_name=BodyPart.RIGHT_HAND,
            item_in_hand=right_hand,
            character=character
        )
        self.left_hand.other_hand = self.right_hand
        self.right_hand.other_hand = self.left_hand

    class ManageHandItem(BaseModel):
        model_config = ConfigDict(
            extra='allow',
            arbitrary_types_allowed=True
        )

        hand_name: BodyPart
        item_in_hand: Equipment | None = None
        other_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, repr=False)
        character: weakref.ref | None = Field(None)

        def equip(self, item: Equipment | None = None) -> (Equipment |
                                                           tuple[Equipment, ...] |
                                                           tuple[None, ...] | None):
            old_item_self: Equipment = self.item_in_hand
            old_item_other: Equipment = self.other_hand.item_in_hand
            if item.type_equipment == EquipmentType.TWO_HAND:
                self.item_in_hand = item
                self.other_hand.item_in_hand = item
                if id(old_item_self) != id(old_item_other):
                    return old_item_self, old_item_other
                return old_item_self
            if old_item_self and old_item_self.type_equipment == EquipmentType.TWO_HAND:
                self.other_hand.item_in_hand = None
            self.item_in_hand = item
            if self.character:
                if self.hand_name == BodyPart.LEFT_HAND:
                    self.character()._left_hand = weakref.ref(item)
                elif self.hand_name == BodyPart.RIGHT_HAND:
                    self.character()._right_hand = weakref.ref(item)
            return old_item_self

        def unequip(self) -> (Equipment |
                              tuple[Equipment, ...] |
                              tuple[None, ...] | None):
            return self.equip(None)


class ArmorFastSlot(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )

    head: 'ArmorFastSlot.ManageArmorItem | None' = Field(None, description='Слот для головы')
    body: 'ArmorFastSlot.ManageArmorItem | None' = Field(None, description='Слот для тела')
    character: weakref.ref | None = Field(None)

    def __init__(self,
                 head: HeadArmor | None = None,
                 body: BodyArmor | None = None,
                 character: weakref.ref | None = None,):
        super().__init__()
        self.head = self.ManageArmorItem(
            body_part_name=BodyPart.HEAD,
            armor=head,
            character=character
        )
        self.body = self.ManageArmorItem(
            body_part_name=BodyPart.BODY,
            armor=body,
            character=character
        )

    class ManageArmorItem(BaseModel):
        model_config = ConfigDict(
            extra='allow',
            arbitrary_types_allowed=True
        )

        body_part_name: BodyPart
        armor: Armor | None = None
        character: weakref.ref | None = Field(None)

        def equip(self, new_armor: Armor | None = None) -> Armor | None:
            if new_armor and self.body_part_name != new_armor.body_part:
                raise ValueError('Броня не подходит под данную часть тела')
            old_armor = self.armor
            self.armor = new_armor
            if self.character:
                if self.body_part_name == BodyPart.HEAD:
                    self.character()._head = weakref.ref(new_armor)
                elif self.body_part_name == BodyPart.BODY:
                    self.character()._body = weakref.ref(new_armor)
            return old_armor

        def unequip(self) -> Armor | None:
            return self.equip(None)