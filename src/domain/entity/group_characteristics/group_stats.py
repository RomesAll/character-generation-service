from dataclasses import dataclass, fields, field

from src.domain.entity.stats.stats import (
    Health,
    HandSkill,
    ActionPoint,
    Bravery,
    Endurance,
    Initiative,
    MeleeDefense,
    ShootingProtection,
    Damage,
    Visibility,
    Moral,
    ShootingSkill,
    DamageArmor,
    HeadHitChance,
)
from src.domain.entity.stats.base import BaseStat
from src.domain.value_object import StatEnum
from src.domain.entity.stats.mapping import MAPPING_STATS


class BuilderStatMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        def create_method(stat_enum_object: StatEnum, stat_object: type["BaseStat"]):
            def wrapper(self, *, current: int, maximum: int):
                setattr(
                    self,
                    "_" + stat_enum_object.value,
                    stat_object(current=current, maximum=maximum),
                )
                return self

            return wrapper

        for stat_enum, stat_obj in MAPPING_STATS.items():
            attrs[stat_enum.value] = create_method(stat_enum, stat_obj)
        return super().__new__(cls, name, bases, attrs)


@dataclass
class GroupStat(metaclass=BuilderStatMeta):
    _health: Health = field(default_factory=Health, init=False)
    _hand_skill: HandSkill = field(default_factory=HandSkill, init=False)
    _action_point: ActionPoint = field(default_factory=ActionPoint, init=False)
    _bravery: Bravery = field(default_factory=Bravery, init=False)
    _endurance: Endurance = field(default_factory=Endurance, init=False)
    _initiative: Initiative = field(default_factory=Initiative, init=False)
    _melee_defense: MeleeDefense = field(default_factory=MeleeDefense, init=False)
    _shooting_protection: ShootingProtection = field(
        default_factory=ShootingProtection, init=False
    )
    _damage: Damage = field(default_factory=Damage, init=False)
    _visibility: Visibility = field(default_factory=Visibility, init=False)
    _moral: Moral = field(default_factory=Moral, init=False)
    _shooting_skill: ShootingSkill = field(
        default_factory=ShootingProtection, init=False
    )
    _damage_armor: DamageArmor = field(default_factory=DamageArmor, init=False)
    _head_hit_chance: HeadHitChance = field(default_factory=HeadHitChance, init=False)
    _level: int = field(default=0, init=False)

    @property
    def level(self) -> int:
        return self._level

    def get_stat(self, stat_enum_object: StatEnum) -> BaseStat:
        return getattr(self, "_" + stat_enum_object.value)

    def increment_level(self, amount: int) -> None:
        if self._level + amount > 3:
            raise ValueError("Level cannot be greater than 3")
        for _ in range(amount):
            self._level += 1
            self.level_up()

    def level_up(self) -> None:
        for current_field in fields(self):
            if current_field.name == "_level":
                continue
            stat: "BaseStat | None" = getattr(self, current_field.name, None)
            if stat and isinstance(stat, BaseStat):
                stat.level_up()
