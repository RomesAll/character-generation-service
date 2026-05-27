from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, PrivateAttr
from enum import Enum
from dataclasses import dataclass, fields

from src.domain.value_object.enums import Measurement

MultiplierObject = tuple[int, Measurement]
MultipliersList = list[MultiplierObject]


class BaseStat(BaseModel, ABC):
    name: 'StatEnum'
    current: int = 0
    maximum: int = 0
    _basic: int = PrivateAttr(default=0)
    _multipliers: MultipliersList = PrivateAttr(default_factory=MultipliersList)

    @abstractmethod
    def append_multipliers(self, multiplier: MultiplierObject):
        self._multipliers.append(multiplier)

    @abstractmethod
    def remove_multipliers(self, multiplier: MultiplierObject):
        delete_object: MultiplierObject | None = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')

    @abstractmethod
    def level_up(self):
        pass

    @property
    def basic(self) -> int:
        return self._basic

    def get_multipliers(self):
        return self._multipliers


class Health(BaseStat):
    current: int = Field(..., ge=0)
    maximum: int = Field(..., ge=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

    def __value_stat_with_multipliers(self) -> int:
        result = self._basic
        for multiplier, measurement in self._multipliers:
            match measurement:
                case Measurement.UNITS:
                    result += multiplier
                case Measurement.PERCENT:
                    result = round(result * (1 + multiplier / 100))
        return result

    def append_multipliers(self, multiplier: MultiplierObject):
        super().append_multipliers(multiplier)
        self.maximum = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: MultiplierObject):
        super().remove_multipliers(multiplier)
        self.maximum = self.__value_stat_with_multipliers()

    def level_up(self):
        self.maximum = self.maximum + 5
        self._basic = self._basic + 5


class HandSkill(BaseStat):
    current: int = Field(..., ge=0, le=100)
    maximum: int = Field(100, ge=100, le=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.current

    def __value_stat_with_multipliers(self) -> int:
        result = self._basic
        for multiplier, measurement in self._multipliers:
            match measurement:
                case Measurement.PERCENT:
                    result += multiplier
        return result

    def append_multipliers(self, multiplier: MultiplierObject):
        super().append_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: MultiplierObject):
        super().remove_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)


class StatEnum(Enum):
    HEALTH = ('health', Health)
    HAND_SKILL = ('hand_skill', HandSkill)


@dataclass
class GroupStat:
    _level: int = 0
    health: Health | None = None
    hand_skill: HandSkill | None = None

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, level: int) -> None:
        if self._level + level <= 3:
            self._level = level

    def level_up(self) -> None:
        self.level = self._level+ 1
        for field in fields(self):
            if field.name == '_level':
                continue
            stat: BaseStat | None = getattr(self, field.name)
            if stat is not None:
                stat.level_up()