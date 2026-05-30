from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaseStat
from src.domain.value_object.enums import Measurement, StatEnum

if TYPE_CHECKING:
    from . import MultiplierObject

class ActionPoints(BaseStat):
    _name: StatEnum = StatEnum.BODY_ARMOR
    current: int = Field(0, ge=0, le=15)
    maximum: int = Field(0, ge=0, le=15)

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

    def append_multipliers(self, multiplier: 'MultiplierObject'):
        super().append_multipliers(multiplier)
        self.current += abs(self.maximum - self.__value_stat_with_multipliers())
        self.maximum = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        super().remove_multipliers(multiplier)
        self.current -= abs(self.maximum - self.__value_stat_with_multipliers())
        self.maximum = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)
