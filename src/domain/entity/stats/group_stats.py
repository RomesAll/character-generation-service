from dataclasses import dataclass, fields, field

from src.domain.value_object.enums import StatEnum
from . import MAPPING_STATS
from .health import Health
from .hand_skill import HandSkill
from .base import BaseStat

class BuilderStatMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        def create_method(stat_enum_object: StatEnum, stat_object: type['BaseStat']):
            def wrapper(self, *, current: int, maximum: int):
                setattr(self,
                        '_' + stat_enum_object.value,
                        stat_object(current=current, maximum=maximum))
                return self
            return wrapper
        for stat_enum, stat_obj in MAPPING_STATS.items():
            attrs[stat_enum.value] = create_method(stat_enum, stat_obj)
        return super().__new__(cls, name, bases, attrs)

@dataclass
class GroupStat(metaclass=BuilderStatMeta):
    _health: Health = field(default_factory=Health, init=False, repr=False)
    _hand_skill: 'HandSkill' = field(default_factory=HandSkill, init=False)
    _level: int = field(default=0, init=False)

    @property
    def level(self) -> int:
        return self._level

    def get_stat(self, stat_enum_object: StatEnum) -> BaseStat:
        return getattr(self, '_' + stat_enum_object.value)

    def increment_level(self, amount: int) -> None:
        if self._level + amount > 3:
            raise ValueError('Level cannot be greater than 3')
        for _ in range(amount):
            self._level += 1
            self.level_up()

    def level_up(self) -> None:
        for current_field in fields(self):
            if current_field.name == '_level':
                continue
            stat: 'BaseStat | None' = getattr(self, current_field.name, None)
            if stat and isinstance(stat, BaseStat):
                stat.level_up()