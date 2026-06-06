from pathlib import Path
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    PrivateAttr,
    computed_field,
)
import uuid, weakref

from src.domain.entity.group_characteristics import GroupStat, GroupPerk
from src.domain.entity.outfits import HeadArmor, BodyArmor, Equipment
from ..fast_slot import ArmsFastSlot, ArmorFastSlot
from ...exceptions import CharacterTypeException, ImageFileException, UnsupportedExtensionException, \
    FileNotFoundException


class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    id: uuid.UUID = Field(..., frozen=True)
    name: str = Field(..., min_length=3, max_length=25)
    image: Path = Field(...)
    _arms_slot: ArmsFastSlot = PrivateAttr(default_factory=ArmsFastSlot)
    _armor_slot: ArmorFastSlot = PrivateAttr(default_factory=ArmorFastSlot)
    _stats: GroupStat = PrivateAttr(default_factory=GroupStat)
    _perks: GroupPerk = PrivateAttr(default_factory=GroupPerk)

    def __init__(
        self,
        *,
        character_id: uuid.UUID,
        name: str,
        image: Path,
        head: HeadArmor | None = None,
        body: BodyArmor | None = None,
        left_hand: Equipment | None = None,
        right_hand: Equipment | None = None,
    ):
        super().__init__(id=character_id, name=name, image=image)
        self.perks.group_stats = weakref.ref(self.stats)
        self.arms_slot.group_stat = weakref.ref(self.stats)
        self.armor_slot.group_stat = weakref.ref(self.stats)
        self.armor_slot.head.equip(head)
        self.armor_slot.body.equip(body)
        if left_hand:
            self.arms_slot.left_hand.equip(left_hand)
        if right_hand:
            self.arms_slot.right_hand.equip(right_hand)

    @computed_field
    @property
    def stats(self) -> GroupStat:
        return self._stats

    @computed_field
    @property
    def perks(self) -> GroupPerk:
        return self._perks

    @computed_field
    @property
    def arms_slot(self) -> ArmsFastSlot:
        return self._arms_slot

    @computed_field
    @property
    def armor_slot(self) -> ArmorFastSlot:
        return self._armor_slot

    @computed_field
    @property
    def head(self) -> HeadArmor:
        return self.armor_slot.head.armor

    @computed_field
    @property
    def body(self) -> BodyArmor:
        return self.armor_slot.body.armor

    @computed_field
    @property
    def left_hand(self) -> Equipment:
        return self.arms_slot.left_hand.item_in_hand

    @computed_field
    @property
    def right_hand(self) -> Equipment:
        return self.arms_slot.right_hand.item_in_hand

    @stats.setter
    def stats(self, value: GroupStat) -> None:
        if not isinstance(value, GroupStat):
            raise CharacterTypeException("Атрибут stats должен быть объектом GroupStat", value)
        self._stats = value
        self.perks.refresh_all_multiplier()

    @perks.setter
    def perks(self, value: GroupPerk) -> None:
        if not isinstance(value, GroupPerk):
            raise CharacterTypeException("Атрибут perks должен быть объектом GroupPerk", value)
        self._stats = self._stats.get_copy_without_multiplier()
        self._perks = value
        self.perks.refresh_all_multiplier()

    @arms_slot.setter
    def arms_slot(self, value: ArmsFastSlot) -> None:
        if not isinstance(value, ArmsFastSlot):
            raise CharacterTypeException("Атрибут arms_slot должен быть объектом ArmsFastSlot", value)
        self._arms_slot = value

    @armor_slot.setter
    def armor_slot(self, value: ArmorFastSlot) -> None:
        if not isinstance(value, ArmorFastSlot):
            raise CharacterTypeException("Атрибут armor_slot должен быть объектом ArmorFastSlot", value)
        self._armor_slot = value

    @field_validator("image", mode="after")
    def validate_image(cls, v: Path):
        if not v.exists():
            raise FileNotFoundException(v)
        if not v.is_file():
            raise ImageFileException(v)
        if v.suffix not in [".png", ".jpg", ".webp"]:
            raise UnsupportedExtensionException(v)
        return v