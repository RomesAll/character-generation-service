from pydantic import BaseModel, Field, ConfigDict

from src.domain.value_object.enums import EquipmentType, BodyPart
from src.domain.entity.arms import Equipment
from src.domain.entity.armor import Armor, HeadArmor, BodyArmor

class ArmsFastSlot(BaseModel):
    model_config = ConfigDict(
        extra='allow'
    )

    left_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, description='Слот под левую руку')
    right_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, description='Слот под правую руку')

    def __init__(self,
                 left_hand: Equipment | None = None,
                 right_hand: Equipment| None = None):
        super().__init__()
        self.left_hand = self.ManageHandItem(hand_name=BodyPart.LEFT_HAND, item_in_hand=left_hand)
        self.right_hand = self.ManageHandItem(hand_name=BodyPart.RIGHT_HAND, item_in_hand=right_hand)
        self.left_hand.other_hand = self.right_hand
        self.right_hand.other_hand = self.left_hand

    class ManageHandItem(BaseModel):
        hand_name: BodyPart
        item_in_hand: Equipment | None = None
        other_hand: 'ArmsFastSlot.ManageHandItem | None' = Field(None, repr=False)

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
            return old_item_self

        def unequip(self) -> (Equipment |
                              tuple[Equipment, ...] |
                              tuple[None, ...] | None):
            return self.equip(None)


class ArmorFastSlot(BaseModel):
    model_config = ConfigDict(
        extra='allow'
    )

    head: 'ArmorFastSlot.ManageArmorItem | None' = Field(None, description='Слот для головы')
    body: 'ArmorFastSlot.ManageArmorItem | None' = Field(None, description='Слот для тела')

    def __init__(self,
                 head: HeadArmor | None = None,
                 body: BodyArmor | None = None):
        super().__init__()
        self.head = self.ManageArmorItem(body_part_name=BodyPart.HEAD, armor=head)
        self.body = self.ManageArmorItem(body_part_name=BodyPart.BODY, armor=body)

    class ManageArmorItem(BaseModel):
        body_part_name: BodyPart
        armor: Armor | None = None

        def equip(self, new_armor: Armor | None = None) -> Armor | None:
            if new_armor and self.body_part_name != new_armor.body_part:
                raise ValueError('Броня не подходит под данную часть тела')
            old_armor = self.armor
            self.armor = new_armor
            return old_armor

        def unequip(self) -> Armor | None:
            return self.equip(None)