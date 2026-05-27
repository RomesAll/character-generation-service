from dataclasses import fields
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import weakref, uuid

from src.domain.entity.fast_slot import ArmsFastSlot, ArmorFastSlot
from src.domain.entity.arms import Arms
from src.domain.entity.armor import HeadArmor, BodyArmor
from src.domain.entity.stats import BaseStat, GroupStat
from src.domain.value_object.perk import Perk

class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              validate_assignment=True,
                              extra='allow')

    id: uuid.UUID = Field(uuid.uuid4(), frozen=True)
    name: str = Field('Bob', min_length=5, max_length=20, frozen=True)

    __stats: GroupStat = PrivateAttr()
    __perks: list[Perk] = PrivateAttr(default_factory=list)

    __head: weakref.ref | None = PrivateAttr(default=None)
    __body: weakref.ref | None = PrivateAttr(default=None)
    __left_hand: weakref.ref | None = PrivateAttr(default=None)
    __right_hand: weakref.ref | None = PrivateAttr(default=None)

    arms_slot: ArmsFastSlot
    armor_slot: ArmorFastSlot
    level: int = Field(0, ge=0, le=3)

    def __init__(self, stats=None, perks=None, **kwargs):
        super().__init__(**kwargs)
        self.__stats = stats
        self.__perks = perks

        if self.armor_slot.head.armor:
            self.__head = weakref.ref(self.armor_slot.head.armor)

        if self.armor_slot.body.armor:
            self.__body = weakref.ref(self.armor_slot.body.armor)

        if self.arms_slot.left_hand.item_in_hand:
            self.__left_hand = weakref.ref(self.arms_slot.left_hand.item_in_hand)

        if self.arms_slot.right_hand.item_in_hand:
            self.__right_hand = weakref.ref(self.arms_slot.right_hand.item_in_hand)

    def take_arms_in_hand(self):
        self.__left_hand = weakref.ref(self.arms_slot.left_hand.item_in_hand)
        self.__right_hand = weakref.ref(self.arms_slot.right_hand.item_in_hand)

    def hide_arms_in_hand(self):
        self.__left_hand = None
        self.__right_hand = None

    @property
    def stats(self) -> GroupStat:
        return self.__stats

    @property
    def perks(self) -> list[Perk]:
        return self.__perks

    @property
    def head(self) -> weakref.ref[HeadArmor] | None:
        return self.__head

    @head.setter
    def head(self, head: weakref.ref[HeadArmor]):
        self.__head = head

    @property
    def body(self) -> weakref.ref[BodyArmor] | None:
        return self.__body

    @body.setter
    def body(self, body: weakref.ref[BodyArmor]):
        self.__body = body

    @property
    def left_hand(self) -> weakref.ref[Arms] | None:
        return self.__left_hand

    @left_hand.setter
    def left_hand(self, left_hand: weakref.ref[Arms]):
        self.__left_hand = left_hand

    @property
    def right_hand(self) -> weakref.ref[Arms] | None:
        return self.__right_hand

    @right_hand.setter
    def right_hand(self, right_hand: weakref.ref[Arms]):
        self.__right_hand = right_hand