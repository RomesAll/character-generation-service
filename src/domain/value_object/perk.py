from dataclasses import dataclass, field

from src.domain.entity.exceptions import InvalidReferenceException, PerkTypeException, StatEnumTypeException, \
    MultiplierAmountTypeException, MeasurementTypeException, NamePerkException, PerkMultiplierException
from src.domain.value_object.enums import Measurement, StatEnum
import weakref

@dataclass(frozen=True)
class PerkMultiplier:
    owner: weakref.ref['Perk']
    stat: StatEnum
    amount: int
    measurement: Measurement

    def __post_init__(self):
        if not isinstance(self.owner, weakref.ref):
            raise InvalidReferenceException(self.owner,f'Класс PerkMultiplier в атрибуте owner ожидает '
                                            f'объект слабой ссылки weakref.ref, передан {type(self.owner)}')
        if not isinstance(self.owner(), Perk):
            raise PerkTypeException(self.owner(), f'Класс PerkMultiplier в атрибуте owner ожидает '
                                                  f'объект слабой ссылки weakref.ref на '
                                                  f'объект класса Perk, передан {type(self.owner())}')
        if not isinstance(self.stat, StatEnum):
            raise StatEnumTypeException(self.stat, f'Класс PerkMultiplier в атрибуте stat ожидает '
                                                  f'объект StatEnum, передан {type(self.stat)}')
        if not isinstance(self.amount, int):
            raise MultiplierAmountTypeException(self.amount, f'Класс PerkMultiplier в атрибуте amount ожидает '
                                                  f'объект int, передан {type(self.amount)}')
        if not isinstance(self.measurement, Measurement):
            raise MeasurementTypeException(self.measurement, f'Класс PerkMultiplier в атрибуте measurement ожидает '
                                                             f'объект Measurement, передан {type(self.measurement)}')

@dataclass(frozen=True)
class Perk:
    name: str
    multipliers: list[PerkMultiplier] = field(default_factory=list)

    def __post_init__(self):
        if not (isinstance(self.name, str) and 3 <= len(self.name) <= 25):
            raise NamePerkException(self.name, 'Название перка в атрибуте name класса Perk должно быть в'
                                    'виде строки, длина которой больше 2, но меньше 26')
        for multiplier in self.multipliers:
            if not isinstance(multiplier, PerkMultiplier):
                raise PerkMultiplierException(f'Список с модификаторами статов ожидает объекты '
                                              f'PerkMultiplier, передан: {type(multiplier)}')
