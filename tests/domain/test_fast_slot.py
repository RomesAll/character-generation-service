from pathlib import Path

import pytest
from src.domain.entity.fast_slot import ArmsFastSlot, ArmorFastSlot
from src.domain.entity.outfits import HeadArmor, BodyArmor, MeleeArms
from src.domain.value_object import EquipmentType, BodyPart


@pytest.fixture(scope="module")
def armor_slot():
    return ArmorFastSlot()


@pytest.fixture(scope="module")
def arms_slot():
    return ArmsFastSlot()


@pytest.fixture(scope="module")
def outfits():
    arms = MeleeArms(
        name="sword",
        type_equipment=EquipmentType.OND_HAND,
        price=10300,
        max_durability=100,
        current_durability=100,
        peculiarities=None,
        image=Path("/dev/null"),
        damage=(34, 44),
        ignore_armor=10,
        damage_armor=15,
        max_endurance=-2,
    )
    arms_two_hand = MeleeArms(
        name="sword",
        type_equipment=EquipmentType.TWO_HAND,
        price=10300,
        max_durability=100,
        current_durability=100,
        peculiarities=None,
        image=Path("/dev/null"),
        damage=(34, 44),
        ignore_armor=10,
        damage_armor=15,
        max_endurance=-2,
    )
    helmet = HeadArmor(
        name="helmet",
        endurance=-3,
        max_durability=100,
        current_durability=100,
        body_part=BodyPart.HEAD,
        image=Path("/dev/null"),
        price=4000,
    )
    plate = BodyArmor(
        name="plate",
        endurance=-13,
        max_durability=100,
        current_durability=100,
        body_part=BodyPart.BODY,
        image=Path("/dev/null"),
        price=2300,
    )
    return {
        "arms": arms,
        "helmet": helmet,
        "plate": plate,
        "arms_two_hand": arms_two_hand,
    }


class TestArmorFastSlot:
    def test_equip(self, armor_slot, outfits):
        copy_armor_slot = armor_slot.model_copy()
        old_helmet = copy_armor_slot.head.equip(item=outfits.get("helmet"))
        assert old_helmet is None
        assert copy_armor_slot.head.armor is outfits.get("helmet")
        old_plate = copy_armor_slot.body.equip(item=outfits.get("plate"))
        assert old_plate is None
        assert copy_armor_slot.body.armor is outfits.get("plate")

    def test_unequip(self, armor_slot, outfits):
        copy_armor_slot = armor_slot.model_copy()
        copy_armor_slot.head.equip(item=outfits.get("helmet"))
        copy_armor_slot.body.equip(item=outfits.get("plate"))
        helmet = copy_armor_slot.head.unequip()
        plate = copy_armor_slot.body.unequip()
        assert helmet is outfits.get("helmet")
        assert plate is outfits.get("plate")
        assert copy_armor_slot.body.armor is None
        assert copy_armor_slot.head.armor is None


class TestArmFastSlot:
    def test_equip(self, arms_slot, outfits):
        copy_arms_slot = arms_slot.model_copy()
        copy_arms_slot.left_hand.equip(item=outfits.get("arms"))
        copy_arms_slot.right_hand.equip(item=outfits.get("arms"))
        assert copy_arms_slot.left_hand.item_in_hand is outfits.get("arms")
        assert copy_arms_slot.right_hand.item_in_hand is outfits.get("arms")