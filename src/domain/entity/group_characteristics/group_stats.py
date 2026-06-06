from dataclasses import dataclass, field
import copy

from src.domain.entity.group_characteristics.metaclasses import BuilderStatMeta
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
    HeadHitChance, HeadArmor, BodyArmor,
)
from src.domain.entity.stats.base import BaseStat
from src.domain.exceptions import LevelException
from src.domain.value_object import StatEnum
from src.domain.value_object.perk import PerkMultiplier


@dataclass
class GroupStat(metaclass=BuilderStatMeta):
    _level: int = field(default=0, init=False)

    _health: Health = field(default_factory=Health, init=False)
    _action_point: ActionPoint = field(default_factory=ActionPoint, init=False)
    _bravery: Bravery = field(default_factory=Bravery, init=False)
    _endurance: Endurance = field(default_factory=Endurance, init=False)
    _initiative: Initiative = field(default_factory=Initiative, init=False)
    _melee_defense: MeleeDefense = field(default_factory=MeleeDefense, init=False)
    _shooting_protection: ShootingProtection = field(default_factory=ShootingProtection, init=False)
    _damage: Damage = field(default_factory=Damage, init=False)
    _visibility: Visibility = field(default_factory=Visibility, init=False)
    _moral: Moral = field(default_factory=Moral, init=False)
    _hand_skill: HandSkill = field(default_factory=HandSkill, init=False)
    _shooting_skill: ShootingSkill = field(default_factory=ShootingSkill, init=False)
    _damage_armor: DamageArmor = field(default_factory=DamageArmor, init=False)
    _head_hit_chance: HeadHitChance = field(default_factory=HeadHitChance, init=False)
    _head_armor: HeadArmor = field(default_factory=HeadArmor, init=False)
    _body_armor: BodyArmor = field(default_factory=BodyArmor, init=False)

    @property
    def level(self) -> int:
        """
        Получить уровень статов
        :return:
        """
        return self._level

    def get_copy(self) -> "GroupStat":
        """
        Получить копию группы статов
        :return:
        """
        return copy.deepcopy(self)

    def get_copy_without_multiplier(self) -> 'GroupStat':
        """
        Получить копию группы статов без модификаторов
        :return:
        """
        copy_obj = copy.copy(self)
        for stat in StatEnum:
            current_stat: BaseStat = getattr(copy_obj, stat.value)
            setattr(copy_obj, '_' + stat.value, current_stat.get_copy_without_multipliers())
        return copy_obj

    def level_up(self) -> None:
        """
        Увеличить уровень
        :return:
        """
        if self._level + 1 > 3:
            raise LevelException(self._level)
        self._level += 1
        for stat in StatEnum:
            current_stat: "BaseStat" = getattr(self, stat.value)
            current_stat.level_up()

    def append_multipliers(self, multiplier: PerkMultiplier):
        """
        Добавить модификатор
        :param multiplier:
        :return:
        """
        stat: BaseStat = getattr(self, multiplier.stat.value)
        stat.append_multipliers(multiplier)

    def remove_multipliers(self, multiplier: PerkMultiplier):
        """
        Удалить модификатор
        :param multiplier:
        :return:
        """
        stat: BaseStat = getattr(self, multiplier.stat.value)
        stat.remove_multipliers(multiplier)
