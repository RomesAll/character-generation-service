from ...value_object import StatEnum
from .stats import (
    Health,
    ActionPoint,
    Bravery,
    Endurance,
    Initiative,
    MeleeDefense,
    ShootingProtection,
    Damage,
    Visibility,
    Moral,
    HandSkill,
    ShootingSkill,
    DamageArmor,
    HeadHitChance,
)

MAPPING_STATS: dict = {
    StatEnum.HEALTH: Health,
    StatEnum.ACTION_POINT: ActionPoint,
    StatEnum.BRAVERY: Bravery,
    StatEnum.ENDURANCE: Endurance,
    StatEnum.INITIATIVE: Initiative,
    StatEnum.MELEE_DEFENSE: MeleeDefense,
    StatEnum.SHOOTING_PROTECTION: ShootingProtection,
    StatEnum.DAMAGE: Damage,
    StatEnum.VISIBILITY: Visibility,
    StatEnum.MORAL: Moral,
    StatEnum.HAND_SKILL: HandSkill,
    StatEnum.SHOOTING_SKILL: ShootingSkill,
    StatEnum.DAMAGE_ARMOR: DamageArmor,
    StatEnum.HEAD_HIT_CHANCE: HeadHitChance,
}
