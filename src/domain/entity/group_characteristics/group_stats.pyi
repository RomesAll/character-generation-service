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
from src.domain.value_object import StatEnum
from src.domain.entity.stats.mapping import MAPPING_STATS
from src.domain.value_object.perk import PerkMultiplier
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from src.domain.entity.characters import Character

@dataclass
class GroupStat:
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
    def level(self) -> int: ...
    def get_copy(self) -> "GroupStat": ...
    def get_copy_without_multiplier(self): ...
    def get_stat(self, stat_enum_object: StatEnum) -> BaseStat: ...
    def level_up(self) -> None: ...
    def append_multipliers(self, multiplier: PerkMultiplier): ...
    def remove_multipliers(self, multiplier: PerkMultiplier): ...
    def health(self, current: int, maximum: int) -> Self: ...
    def action_point(self, current: int, maximum: int) -> Self: ...
    def bravery(self, current: int, maximum: int) -> Self: ...
    def endurance(self, current: int, maximum: int) -> Self: ...
    def initiative(self, current: int, maximum: int) -> Self: ...
    def melee_defense(self, current: int, maximum: int) -> Self: ...
    def shooting_protection(self, current: int, maximum: int) -> Self: ...
    def damage(self, current: int, maximum: int) -> Self: ...
    def visibility(self, current: int, maximum: int) -> Self: ...
    def moral(self, current: int, maximum: int) -> Self: ...
    def hand_skill(self, current: int, maximum: int) -> Self: ...
    def shooting_skill(self, current: int, maximum: int) -> Self: ...
    def damage_armor(self, current: int, maximum: int) -> Self: ...
    def head_hit_chance(self, current: int, maximum: int) -> Self: ...
