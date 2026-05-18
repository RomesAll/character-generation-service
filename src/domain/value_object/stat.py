from dataclasses import dataclass, field

@dataclass(frozen=True)
class Stat:
    health: int = field(default=0, metadata={'description': 'Health'})
    armor_head: int = field(default=0, metadata={'description': 'Armor head'})
    armor_body: int = field(default=0, metadata={'description': 'Armor body'})
    action_points: int = field(default=0, metadata={'description': 'Action points'})
    endurance: int = field(default=0, metadata={'description': 'Endurance'})
    moral: int = field(default=0, metadata={'description': 'Moral'})
    courage: int = field(default=0, metadata={'description': 'Courage'})
    hand_scourge: int = field(default=0, metadata={'description': 'Hand scourge'})
    shooting_skill: int = field(default=0, metadata={'description': 'Shooting skill'})
    hand_protection: int = field(default=0, metadata={'description': 'Hand protection'})
    shooting_protection: int = field(default=0, metadata={'description': 'Shooting protection'})
    damage: int = field(default=0, metadata={'description': 'Damage'})
    damage_armor: int = field(default=0, metadata={'description': 'Damage armor'})
    head_hit_chance: int = field(default=0, metadata={'description': 'Head hit chance'})
    visibility: int = field(default=0, metadata={'description': 'Visibility'})