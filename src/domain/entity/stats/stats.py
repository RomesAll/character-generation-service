from pydantic import Field
from .base import UnitStat, PercentStat
from src.domain.value_object import StatEnum


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


class Damage(UnitStat):
    current: int = Field(default=0, ge=0, le=220)
    maximum: int = Field(default=0, ge=0, le=220)
    name: "StatEnum" = StatEnum.DAMAGE


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
