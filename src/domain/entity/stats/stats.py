from typing import TYPE_CHECKING
from pydantic import Field, PrivateAttr
from src.domain.entity.stats import BaseStat
from src.domain.value_object import StatEnum, Measurement

if TYPE_CHECKING:
    from . import MultiplierObject

class Health(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.HEALTH

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class ActionPoint(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.ACTION_POINT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Bravery(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.BRAVERY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Endurance(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.ENDURANCE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Initiative(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.INITIATIVE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class MeleeDefense(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.MELEE_DEFENSE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class ShootingProtection(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.SHOOTING_PROTECTION

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Damage(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.DAMAGE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Visibility(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.VISIBILITY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class Moral(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.MORAL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._basic = self.maximum

class HandSkill(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.HAND_SKILL

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
        self._multipliers.append(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        delete_object: 'MultiplierObject | None' = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)

class ShootingSkill(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.SHOOTING_SKILL

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
        self._multipliers.append(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        delete_object: 'MultiplierObject | None' = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)

class DamageArmor(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.DAMAGE_ARMOR

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
        self._multipliers.append(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        delete_object: 'MultiplierObject | None' = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)

class HeadHitChance(BaseStat):
    current: int = Field(default=0, ge=0)
    maximum: int = Field(default=0, ge=0)
    _name: 'StatEnum' = StatEnum.HEAD_HIT_CHANCE

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
        self._multipliers.append(multiplier)
        self.current = self.__value_stat_with_multipliers()

    def remove_multipliers(self, multiplier: 'MultiplierObject'):
        delete_object: 'MultiplierObject | None' = None
        for ind, obj in enumerate(start=0, iterable=self._multipliers):
            if obj[0] == multiplier[0] and obj[1] == multiplier[1]:
                delete_object = self._multipliers.pop(ind)
                break
        if not delete_object:
            raise ValueError(f'Multiplier {multiplier} not found')
        self.current = self.__value_stat_with_multipliers()

    def level_up(self):
        self.current = min(self.current + 5, 100)