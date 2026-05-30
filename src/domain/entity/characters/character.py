from pathlib import Path

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import weakref, uuid

from src.domain.entity.characters.fast_slot import ArmsFastSlot, ArmorFastSlot
from src.domain.entity.stats.group_stats import GroupStat
from src.domain.value_object.perk import GroupPerk

class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              validate_assignment=True,
                              extra='allow')

    id: uuid.UUID = Field(uuid.uuid4(), frozen=True)
    name: str = Field('Bob', min_length=5, max_length=20, frozen=True)

    head_img: Path
    body_img: Path

    arms_slot: ArmsFastSlot | None = Field(default=None)
    armor_slot: ArmorFastSlot | None = Field(default=None)

    _stats: GroupStat = PrivateAttr(default_factory=GroupStat)
    _perks: GroupPerk = PrivateAttr(default_factory=GroupPerk)

    _head: weakref.ref | None = PrivateAttr(default=None)
    _body: weakref.ref | None = PrivateAttr(default=None)
    _left_hand: weakref.ref | None = PrivateAttr(default=None)
    _right_hand: weakref.ref | None = PrivateAttr(default=None)

    def __init__(self, name: str, head: Path, body: Path):
        super().__init__(name=name, head_img=head, body_img=body)
        self._perks.character = weakref.ref(self)
        self.armor_slot = ArmorFastSlot(character=weakref.ref(self))
        self.arms_slot = ArmsFastSlot(character=weakref.ref(self))

    @property
    def stats(self):
        return self._stats

    @property
    def perk(self):
        return self._perks

    @property
    def head(self):
        return self._head() if self._head else None

    @property
    def body(self):
        return self._body() if self._body else None

    @property
    def left_hand(self):
        return self._left_hand() if self._left_hand else None

    @property
    def right_hand(self):
        return self._right_hand() if self._right_hand else None