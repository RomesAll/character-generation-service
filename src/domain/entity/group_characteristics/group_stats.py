import copy
import weakref
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
from src.domain.exceptions import LevelException
from src.domain.value_object import StatEnum
from src.domain.entity.stats.mapping import MAPPING_STATS
from src.domain.value_object.perk import PerkMultiplier
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.characters import Character


class BuilderStatMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        def create_method(stat_enum_object: StatEnum, stat_object: type["BaseStat"]):
            def wrapper(self, *, current: int, maximum: int):
                stat: BaseStat = getattr(self, "_" + stat_enum_object.value)
                new_object: BaseStat = stat_object(current=current, maximum=maximum)
                setattr(self, "_" + stat_enum_object.value, new_object)
                for multiplier in stat.multipliers:
                    self.append_multipliers(multiplier)
                return self

            return wrapper

        for stat_enum, stat_obj in MAPPING_STATS.items():
            attrs[stat_enum.value] = create_method(stat_enum, stat_obj)
        return super().__new__(cls, name, bases, attrs)


@dataclass
class GroupStat(metaclass=BuilderStatMeta):
    _health: Health = field(
        default_factory=lambda: Health(
            current=65,
            maximum=65,
        ),
        init=False,
    )
    _action_point: ActionPoint = field(
        default_factory=lambda: ActionPoint(
            current=6,
            maximum=6,
        ),
        init=False,
    )
    _bravery: Bravery = field(
        default_factory=lambda: Bravery(
            current=100,
            maximum=100,
        ),
        init=False,
    )
    _endurance: Endurance = field(
        default_factory=lambda: Endurance(
            current=53,
            maximum=53,
        ),
        init=False,
    )
    _initiative: Initiative = field(
        default_factory=lambda: Initiative(
            current=100,
            maximum=100,
        ),
        init=False,
    )
    _melee_defense: MeleeDefense = field(
        default_factory=lambda: MeleeDefense(
            current=50,
            maximum=50,
        ),
        init=False,
    )
    _shooting_protection: ShootingProtection = field(
        default_factory=lambda: ShootingProtection(
            current=50,
            maximum=50,
        ),
        init=False,
    )
    _damage: Damage = field(
        default_factory=lambda: Damage(
            current=0,
            maximum=0,
        ),
        init=False,
    )
    _visibility: Visibility = field(
        default_factory=lambda: Visibility(
            current=9,
            maximum=9,
        ),
        init=False,
    )
    _moral: Moral = field(
        default_factory=lambda: Moral(
            current=100,
            maximum=100,
        ),
        init=False,
    )
    _hand_skill: HandSkill = field(
        default_factory=lambda: HandSkill(
            current=30,
        ),
        init=False,
    )
    _shooting_skill: ShootingSkill = field(
        default_factory=lambda: ShootingSkill(
            current=10,
        ),
        init=False,
    )
    _damage_armor: DamageArmor = field(
        default_factory=lambda: DamageArmor(
            current=150,
        ),
        init=False,
    )
    _head_hit_chance: HeadHitChance = field(
        default_factory=lambda: HeadHitChance(current=25), init=False
    )
    _level: int = field(default=0, init=False)
    _character: weakref.ref["Character"] | None = field(default=None, init=False)

    @property
    def level(self) -> int:
        return self._level

    def get_copy(self) -> "GroupStat":
        return copy.deepcopy(self)

    def get_copy_without_multiplier(self):
        copy_obj = copy.copy(self)
        for field_stat in fields(self):
            stat: BaseStat = getattr(copy_obj, field_stat.name)
            setattr(copy_obj, field_stat.name, stat.get_copy_without_multipliers())

    def get_stat(self, stat_enum_object: StatEnum) -> BaseStat:
        return getattr(self, "_" + stat_enum_object.value)

    def increment_level(self, amount: int) -> None:
        if self._level + amount > 3:
            raise LevelException(self._level)
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

    def append_multipliers(self, multiplier: PerkMultiplier):
        stat: BaseStat = getattr(self, "_" + multiplier.stat.value)
        stat.append_multipliers(multiplier)

    def remove_multipliers(self, multiplier: PerkMultiplier):
        stat: BaseStat = getattr(self, "_" + multiplier.stat.value)
        stat.remove_multipliers(multiplier)
