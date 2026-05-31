from abc import ABC

from pydantic import BaseModel, PrivateAttr, Field, model_validator

from src.domain.value_object.enums import StatEnum, Measurement
from src.domain.value_object.perk import PerkMultiplier


class BaseStat(BaseModel, ABC):
    name: StatEnum = Field(..., frozen=True)
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _basic: int = PrivateAttr(default=0)
    _multipliers: list[PerkMultiplier] = PrivateAttr(default_factory=list)

    @model_validator(mode="after")
    def validate_current_value(self):
        if self.current > self.maximum:
            raise ValueError("Current value cannot be greater than maximum")
        return self

    @property
    def basic(self) -> int:
        return self._basic

    @property
    def multipliers(self):
        return self._multipliers.copy()

    def append_multipliers(self, multiplier: PerkMultiplier):
        self._multipliers.append(multiplier)

    def remove_multipliers(self, multiplier: PerkMultiplier):
        delete_object: PerkMultiplier | None = None
        for ind, perk_multiplier in enumerate(start=0, iterable=self._multipliers):
            if perk_multiplier == multiplier:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f"Multiplier {multiplier} not found")


class UnitStat(BaseStat, ABC):
    current: int = Field(default=0, ge=500)
    maximum: int = Field(default=0, ge=500)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

    def value_stat_with_multipliers(self) -> int:
        result = self._basic
        for multiplier, measurement in self._multipliers:
            match measurement:
                case Measurement.UNITS:
                    result += multiplier
                case Measurement.PERCENT:
                    result = round(result * (1 + multiplier / 100))
        return result

    def append_multipliers(self, multiplier: PerkMultiplier):
        super().append_multipliers(multiplier)
        self.maximum = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: PerkMultiplier):
        super().remove_multipliers(multiplier)
        self.maximum = self.__value_stat_with_multipliers()

    def level_up(self):
        self.maximum = self.maximum + 5
        self._basic = self._basic + 5


class PercentStat(BaseStat, ABC):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.current

    def value_stat_with_multipliers(self) -> int:
        result = self._basic
        for multiplier, measurement in self._multipliers:
            match measurement:
                case Measurement.PERCENT:
                    result += multiplier
        return result

    def append_multipliers(self, multiplier: PerkMultiplier):
        super().append_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: PerkMultiplier):
        super().remove_multipliers(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)
