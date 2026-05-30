from abc import ABC
from pydantic import BaseModel, PrivateAttr, Field, model_validator
from typing import TYPE_CHECKING

from src.domain.value_object.enums import StatEnum, Measurement

if TYPE_CHECKING:
    from . import MultipliersList, MultiplierObject

class BaseStat(BaseModel, ABC):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = PrivateAttr()
    _basic: int = PrivateAttr(default=0)
    _multipliers: 'MultipliersList' = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_current_value(self):
        if self.current > self.maximum:
            raise ValueError('Current value cannot be greater than maximum')
        return self

    def append_multipliers(self, multiplier: 'MultiplierObject'):
        self._multipliers.append(multiplier)
        self.maximum = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        delete_object: 'MultiplierObject | None' = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')
        self.maximum = self.__value_stat_with_multipliers()

    def __value_stat_with_multipliers(self) -> int:
        result = self._basic
        for multiplier, measurement in self._multipliers:
            match measurement:
                case Measurement.UNITS:
                    result += multiplier
                case Measurement.PERCENT:
                    result = round(result * (1 + multiplier / 100))
        return result

    def level_up(self):
        self.maximum = self.maximum + 5
        self._basic = self._basic + 5

    @property
    def basic(self) -> int:
        return self._basic

    @property
    def multipliers(self):
        return self._multipliers

    @property
    def name(self):
        return self._name