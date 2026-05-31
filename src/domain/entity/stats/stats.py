from pydantic import Field
from .base import UnitStat, PercentStat
from src.domain.value_object import StatEnum


class Health(UnitStat):
    current: int = Field(default=0, ge=150)
    maximum: int = Field(default=0, ge=150)
    _name: "StatEnum" = StatEnum.HEALTH


class ActionPoint(UnitStat):
    current: int = Field(default=0, ge=15)
    maximum: int = Field(default=0, ge=15)
    _name: "StatEnum" = StatEnum.ACTION_POINT


class Bravery(UnitStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.BRAVERY


class Endurance(UnitStat):
    current: int = Field(default=0, ge=73)
    maximum: int = Field(default=0, ge=73)
    _name: "StatEnum" = StatEnum.ENDURANCE


class Initiative(UnitStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.INITIATIVE


class MeleeDefense(UnitStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.MELEE_DEFENSE


class ShootingProtection(UnitStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.SHOOTING_PROTECTION


class Damage(UnitStat):
    current: int = Field(default=0, ge=200)
    maximum: int = Field(default=0, ge=200)
    _name: "StatEnum" = StatEnum.DAMAGE


class Visibility(UnitStat):
    current: int = Field(default=0, ge=10)
    maximum: int = Field(default=0, ge=10)
    _name: "StatEnum" = StatEnum.VISIBILITY


class Moral(UnitStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.MORAL


class HandSkill(PercentStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.HAND_SKILL


class ShootingSkill(PercentStat):
    current: int = Field(default=0, ge=100)
    maximum: int = Field(default=0, ge=100)
    _name: "StatEnum" = StatEnum.SHOOTING_SKILL


class DamageArmor(PercentStat):
    current: int = Field(default=0, ge=200)
    maximum: int = Field(default=0, ge=200)
    _name: "StatEnum" = StatEnum.DAMAGE_ARMOR


class HeadHitChance(PercentStat):
    current: int = Field(default=0, ge=90)
    maximum: int = Field(default=0, ge=90)
    _name: "StatEnum" = StatEnum.HEAD_HIT_CHANCE
