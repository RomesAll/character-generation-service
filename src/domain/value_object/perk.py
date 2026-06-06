from dataclasses import dataclass, field
import weakref

from src.domain.exceptions import (
    StatEnumTypeException,
    MultiplierAmountTypeException,
    MeasurementTypeException,
    NamePerkException,
    PerkMultiplierException,
)
from src.domain.value_object.enums import Measurement, StatEnum

@dataclass(frozen=True)
class PerkMultiplier:
    stat: StatEnum
    amount: int
    measurement: Measurement
    _owner_ref: weakref.ref["Perk"] | None = field(default=None, init=False)

    def __post_init__(self):
        if not isinstance(self.stat, StatEnum):
            raise StatEnumTypeException(
                self.stat,
                f"Класс PerkMultiplier в атрибуте stat ожидает "
                f"объект StatEnum, передан {type(self.stat)}",
            )
        if not isinstance(self.amount, int):
            raise MultiplierAmountTypeException(
                self.amount,
                f"Класс PerkMultiplier в атрибуте amount ожидает "
                f"объект int, передан {type(self.amount)}",
            )
        if not isinstance(self.measurement, Measurement):
            raise MeasurementTypeException(
                self.measurement,
                f"Класс PerkMultiplier в атрибуте measurement ожидает "
                f"объект Measurement, передан {type(self.measurement)}",
            )

    @property
    def owner(self):
        return self._owner_ref() if self._owner_ref else None


@dataclass(frozen=True)
class Perk:
    name: str
    multipliers: tuple["PerkMultiplier", ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not (isinstance(self.name, str) and 3 <= len(self.name) <= 25):
            raise NamePerkException(
                self.name,
                "Название перка в атрибуте name класса Perk должно быть в"
                "виде строки, длина которой больше 2, но меньше 26",
            )
        for multiplier in self.multipliers:
            if not isinstance(multiplier, PerkMultiplier):
                raise PerkMultiplierException(
                    f"Список с модификаторами статов ожидает объекты "
                    f"PerkMultiplier, передан: {type(multiplier)}"
                )

            object.__setattr__(multiplier, "_owner_ref", weakref.ref(self))