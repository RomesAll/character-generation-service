from pydantic import Field, model_validator
from .base import UnitStat, PercentStat
from src.domain.value_object import StatEnum
from ...exceptions import CurrentGreaterMaximumException

min_damage = int
max_damage = int

class Health(UnitStat):
    current: int = Field(default=0, ge=0, le=200)
    maximum: int = Field(default=0, ge=0, le=200)
    name: "StatEnum" = StatEnum.HEALTH


class ActionPoint(UnitStat):
    current: int = Field(default=0, ge=0, le=15)
    maximum: int = Field(default=0, ge=0, le=15)
    name: "StatEnum" = StatEnum.ACTION_POINT


class Bravery(UnitStat):
    current: int = Field(default=0, ge=0, le=150)
    maximum: int = Field(default=0, ge=0, le=150)
    name: "StatEnum" = StatEnum.BRAVERY


class Endurance(UnitStat):
    current: int = Field(default=0, ge=0, le=80)
    maximum: int = Field(default=0, ge=0, le=80)
    name: "StatEnum" = StatEnum.ENDURANCE


class Initiative(UnitStat):
    current: int = Field(default=0, ge=0, le=120)
    maximum: int = Field(default=0, ge=0, le=120)
    name: "StatEnum" = StatEnum.INITIATIVE


class MeleeDefense(UnitStat):
    current: int = Field(default=0, ge=0, le=150)
    maximum: int = Field(default=0, ge=0, le=150)
    name: "StatEnum" = StatEnum.MELEE_DEFENSE


class ShootingProtection(UnitStat):
    current: int = Field(default=0, ge=0, le=150)
    maximum: int = Field(default=0, ge=0, le=150)
    name: "StatEnum" = StatEnum.SHOOTING_PROTECTION

class HeadArmor(UnitStat):
    current: int = Field(default=0, ge=0, le=400)
    maximum: int = Field(default=0, ge=0, le=400)
    name: "StatEnum" = StatEnum.HEAD_ARMOR


class BodyArmor(UnitStat):
    current: int = Field(default=0, ge=0, le=600)
    maximum: int = Field(default=0, ge=0, le=600)
    name: "StatEnum" = StatEnum.BODY_ARMOR


class Damage(UnitStat):
    current: tuple[min_damage, max_damage] = Field(default=(0, 0))
    maximum: max_damage = Field(default=0, ge=0, le=400)
    name: "StatEnum" = StatEnum.DAMAGE

    @model_validator(mode="after")
    def validate_current_value(self):
        if self.current[1] > self.maximum:
            raise CurrentGreaterMaximumException(f"Текущее значение стата {self.current} не "
                                        f"может быть больше максимального {self.maximum}")
        return self

class Visibility(UnitStat):
    current: int = Field(default=0, ge=0, le=10)
    maximum: int = Field(default=0, ge=0, le=10)
    name: "StatEnum" = StatEnum.VISIBILITY


class Moral(UnitStat):
    current: int = Field(default=0, ge=0, le=130)
    maximum: int = Field(default=0, ge=0, le=130)
    name: "StatEnum" = StatEnum.MORAL


class HandSkill(PercentStat):
    current: int = Field(default=0, ge=0, le=100)
    maximum: int = Field(default=100, ge=0, le=100)
    name: "StatEnum" = StatEnum.HAND_SKILL


class ShootingSkill(PercentStat):
    current: int = Field(default=0, ge=0, le=100)
    maximum: int = Field(default=100, ge=0, le=100)
    name: "StatEnum" = StatEnum.SHOOTING_SKILL


class DamageArmor(PercentStat):
    current: int = Field(default=0, ge=0, le=200)
    maximum: int = Field(default=200, ge=0,le=200)
    name: "StatEnum" = StatEnum.DAMAGE_ARMOR


class HeadHitChance(PercentStat):
    current: int = Field(default=0, ge=0, le=100)
    maximum: int = Field(default=100, ge=0, le=100)
    name: "StatEnum" = StatEnum.HEAD_HIT_CHANCE
