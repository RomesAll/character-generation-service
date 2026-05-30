from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .health import Health
from .hand_skill import HandSkill

if TYPE_CHECKING:
    from ...value_object.enums import StatEnum
    from .base import BaseStat

@dataclass
class GroupStat:
    _health: Health = field(default_factory=Health, init=False, repr=False)
    _hand_skill: 'HandSkill' = field(default_factory=HandSkill, init=False)
    _level: int = field(default=0, init=False)

    @property
    def level(self) -> int: ...

    def get_stat(self, stat_enum_object: 'StatEnum') -> 'BaseStat': ...

    def increment_level(self, amount: int) -> None: ...

    def level_up(self) -> None: ...

    def health(self, *, current: int, maximum: int) -> GroupStat: ...

    def hand_skill(self, *, current: int, maximum: int) -> GroupStat: ...