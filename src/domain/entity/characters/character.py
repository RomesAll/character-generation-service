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

from .fast_slot import ArmsFastSlot, ArmorFastSlot
from src.domain.entity.group_characteristics import GroupStat, GroupPerk
from src.domain.entity.outfits import HeadArmor, BodyArmor, Equipment, Arms, MeleeArms


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
        self._stats._character = weakref.ref(self)
        self._perks._character = weakref.ref(self)
        self._arms_slot._character = weakref.ref(self)
        self._armor_slot._character = weakref.ref(self)
        self._armor_slot.head.equip(head)
        self._armor_slot.body.equip(body)
        if left_hand:
            self._arms_slot.left_hand.equip(left_hand)
        if right_hand:
            self._arms_slot.right_hand.equip(right_hand)

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
            raise TypeError("stats must be GroupStat")
        self._stats = value
        self.perks.add_all_multiplier()

    @perks.setter
    def perks(self, value: GroupPerk) -> None:
        if not isinstance(value, GroupPerk):
            raise TypeError("perks must be GroupPerk")
        self._stats = self._stats.get_copy_without_multiplier()
        self._perks = value
        self.perks.add_all_multiplier()

    @arms_slot.setter
    def arms_slot(self, value: ArmsFastSlot) -> None:
        if not isinstance(value, ArmsFastSlot):
            raise TypeError("arms_slot must be ArmsFastSlot")
        self._arms_slot = value

    @armor_slot.setter
    def armor_slot(self, value: ArmorFastSlot) -> None:
        if not isinstance(value, ArmorFastSlot):
            raise TypeError("armor_slot must be ArmorFastSlot")
        self._armor_slot = value

    @field_validator("image", mode="after")
    def validate_image(cls, v: Path):
        if not v.is_file():
            raise FileNotFoundError("Image must be a file")
        if v.suffix not in [".png", ".jpg", ".webp"]:
            raise ValueError("Image must be a .png or .jpg image")
        return v