from pathlib import Path
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    PrivateAttr,
    computed_field,
)
import copy, uuid, weakref

from .fast_slot import ArmsFastSlot, ArmorFastSlot
from src.domain.entity.group_characteristics import GroupStat, GroupPerk, AmountPerk
from src.domain.entity.outfits import HeadArmor, BodyArmor, Equipment, Arms, MeleeArms
from src.domain.entity.stats import BaseStat
from src.domain.entity.group_characteristics import NamePerk
from src.domain.value_object import StatEnum, Measurement
from src.domain.value_object.perk import Perk


class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    id: uuid.UUID = Field(..., frozen=True)
    name: str = Field(..., min_length=3, max_length=25)
    image: Path = Field(...)
    _stats: GroupStat = PrivateAttr(default_factory=GroupStat)
    _perks: GroupPerk = PrivateAttr(default_factory=GroupPerk)
    _arms_slot: ArmsFastSlot = PrivateAttr(default_factory=ArmsFastSlot)
    _armor_slot: ArmorFastSlot = PrivateAttr(default_factory=ArmorFastSlot)
    _head: weakref.ref[HeadArmor] | None = PrivateAttr(default=None)
    _body: weakref.ref[BodyArmor] | None = PrivateAttr(default=None)
    _left_hand: weakref.ref[Equipment | Arms] | None = PrivateAttr(default=None)
    _right_hand: weakref.ref[Equipment | Arms] | None = PrivateAttr(default=None)

    def __init__(
        self,
        *,
        character_id: uuid.UUID,
        name: str,
        image: Path,
        stats: GroupStat | None = None,
        perks: GroupPerk | None = None,
        arms_slot: ArmsFastSlot | None = None,
        armor_slot: ArmorFastSlot | None = None,
    ):
        super().__init__(id=character_id, name=name, image=image)
        if stats:
            self.stats = stats
        if perks:
            self.perks = perks
        if arms_slot:
            self.arms_slot = arms_slot
            self._left_hand = weakref.ref(self._arms_slot.left_hand.item_in_hand)
            self._right_hand = weakref.ref(self._arms_slot.right_hand.item_in_hand)
        if armor_slot:
            self.armor_slot = armor_slot
            self._head = weakref.ref(armor_slot.head.armor)
            self._body = weakref.ref(armor_slot.body.armor)

        self._aboba = '12'

    @computed_field
    @property
    def stats(self) -> GroupStat:
        return copy.deepcopy(self._stats)

    @computed_field
    @property
    def perks(self) -> GroupPerk:
        return copy.deepcopy(self._perks)

    @computed_field
    @property
    def arms_slot(self) -> ArmsFastSlot:
        return copy.deepcopy(self._arms_slot)

    @computed_field
    @property
    def armor_slot(self) -> ArmorFastSlot:
        return copy.deepcopy(self._armor_slot)

    @computed_field
    @property
    def head(self) -> HeadArmor:
        return self._head() if self._head else None

    @computed_field
    @property
    def body(self) -> BodyArmor:
        return self._body() if self._body else None

    @computed_field
    @property
    def left_hand(self) -> Equipment:
        return self._left_hand() if self._left_hand else None

    @computed_field
    @property
    def right_hand(self) -> Equipment:
        return self._right_hand() if self._right_hand else None

    @stats.setter
    def stats(self, value: GroupStat) -> None:
        if not isinstance(value, GroupStat):
            raise TypeError("stats must be GroupStat")
        self._stats = copy.deepcopy(value)
        self.__add_all_multiplier()

    @perks.setter
    def perks(self, value: GroupPerk) -> None:
        if not isinstance(value, GroupPerk):
            raise TypeError("perks must be GroupPerk")
        self.__remove_all_multiplier()
        self._perks = copy.deepcopy(value)
        self.__add_all_multiplier()

    @arms_slot.setter
    def arms_slot(self, value: ArmsFastSlot) -> None:
        if not isinstance(value, ArmsFastSlot):
            raise TypeError("arms_slot must be ArmsFastSlot")
        self._arms_slot = copy.deepcopy(value)

    @armor_slot.setter
    def armor_slot(self, value: ArmorFastSlot) -> None:
        if not isinstance(value, ArmorFastSlot):
            raise TypeError("armor_slot must be ArmorFastSlot")
        self._armor_slot = copy.deepcopy(value)

    @field_validator("image", mode="after")
    def validate_image(cls, v: Path):
        if not v.is_file():
            raise FileNotFoundError("Image must be a file")
        if v.suffix not in [".png", ".jpg", ".webp"]:
            raise ValueError("Image must be a .png or .jpg image")
        return v

    def set_head(self, value: HeadArmor) -> HeadArmor | None:
        if value and not isinstance(value, HeadArmor):
            raise TypeError("head must be HeadArmor")
        old_head = self._armor_slot.head.equip(value)
        self._head = weakref.ref(value)
        return old_head

    def set_body(self, value: BodyArmor) -> BodyArmor | None:
        if value and not isinstance(value, BodyArmor):
            raise TypeError("body must be BodyArmor")
        old_body = self._armor_slot.body.equip(value)
        self._body = weakref.ref(value)
        return old_body

    def set_left_hand(self, value: Equipment | Arms) -> Equipment | None:
        if value and not isinstance(value, Equipment):
            raise TypeError("left_hand must be Equipment")
        old_left_hand = self._arms_slot.left_hand.equip(value)
        self._left_hand = weakref.ref(value)
        if type(value) is MeleeArms:
            self._stats.damage(current=value.damage, maximum=value.damage)
        return old_left_hand

    def set_right_hand(self, value: Equipment) -> Equipment | None:
        if value and not isinstance(value, Equipment):
            raise TypeError("right_hand must be Equipment")
        old_right_hand = self._arms_slot.right_hand.equip(value)
        self._right_hand = weakref.ref(value)
        if type(value) is MeleeArms:
            self._stats.damage(current=value.damage, maximum=value.damage)
        return old_right_hand

    def take_off_from_head(self):
        old_head = self._armor_slot.head.unequip()
        self._head = None
        return old_head

    def take_off_from_body(self):
        old_body = self._armor_slot.body.unequip()
        self._body = None
        return old_body

    def take_off_from_left_hand(self):
        old_left_hand_item = self._arms_slot.left_hand.unequip()
        self._left_hand = None
        if type(self._left_hand()) is Arms:
            self._stats.damage(current=self._left_hand().damage,
                               maximum=self._left_hand().damage)
        return old_left_hand_item

    def take_off_from_right_hand(self):
        old_right_hand_item = self._arms_slot.right_hand.unequip()
        self._right_hand = None
        if type(self._right_hand()) is Arms:
            self._stats.damage(current=self._right_hand().damage,
                               maximum=self._right_hand().damage)
        return old_right_hand_item

    def add_perk(self, name: NamePerk, stats: list[tuple[StatEnum, AmountPerk, Measurement]]):
        self._perks.add(name=name, stats=stats)
        added_perk: Perk = self._perks.get_perk_by_name(name, direction='right')
        self.__add_multiplier(added_perk)

    def pop_perk(self, name: NamePerk):
        delete_perk: Perk = self._perks.get_perk_by_name(name)
        self.__remove_multiplier(delete_perk)
        self._perks.remove(name=NamePerk(delete_perk.name))
        return delete_perk

    def __remove_multiplier(self, perk: Perk):
        for multiplier in perk.multipliers:
            stat_obj: BaseStat = self._stats.get_stat(multiplier.stat)
            stat_obj.remove_multipliers(multiplier)

    def __remove_all_multiplier(self):
        for perk in self._perks.perks:
            self.__remove_multiplier(perk=perk)

    def __add_multiplier(self, perk: Perk):
        for multiplier in perk.multipliers:
            stat_obj: BaseStat = self._stats.get_stat(multiplier.stat)
            stat_obj.append_multipliers(multiplier)

    def __add_all_multiplier(self):
        for perk in self._perks.perks:
            self.__add_multiplier(perk=perk)
