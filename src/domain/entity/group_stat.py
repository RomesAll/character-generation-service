from dataclasses import dataclass
from src.domain.value_object.stat import (
    Health,
    ArmorHead,
    ArmorBody,
    ActionPoint,
    Endurance,
    Moral,
    Courage,
    HandScourge,
    ShootingSkill,
    HandProtection,
    ShootingProtection,
    Damage,
    DamageArmor,
    HeadHitChance,
    Visibility,
)

@dataclass
class GroupStat:
    health: Health
    armor_head: ArmorHead
    armor_body: ArmorBody
    action_points: ActionPoint
    endurance: Endurance
    moral: Moral
    courage: Courage
    hand_scourge: HandScourge
    shooting_skill: ShootingSkill
    hand_protection: HandProtection
    shooting_protection: ShootingProtection
    damage: Damage
    damage_armor: DamageArmor
    head_hit_chance: HeadHitChance
    visibility: Visibility