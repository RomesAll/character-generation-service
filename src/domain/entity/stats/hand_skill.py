from pydantic import Field
from typing import TYPE_CHECKING

from .base import BaseStat
from src.domain.value_object.enums import Measurement, StatEnum

if TYPE_CHECKING:
    from . import MultiplierObject

class HandSkill(BaseStat):
    current: int = Field(0, ge=0, le=100)
    maximum: int = Field(100, ge=100, le=100)
    _name: StatEnum = StatEnum.HAND_SKILL

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

    def append_multipliers(self, multiplier: 'MultiplierObject'):
        super().append_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        super().remove_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)
