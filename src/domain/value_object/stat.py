from dataclasses import dataclass, field

@dataclass(frozen=True)
class BaseStat:
    name: str
    current: int
    maximum: int
    description: str | None = None

    def __post_init__(self):
        if self.maximum <= 0:
            raise ValueError('Максимальное значение должно быть больше 0')
        if not(0 <= self.current <= self.maximum):
            raise ValueError(f'Текущее значение характеристики: {self.name} должно находится в '
                             f'диапазоне от 0 до {self.maximum}')

    def decrease(self, damage: int) -> 'BaseStat':
        new_current_value = max(0, self.current - damage)
        return BaseStat(self.name, new_current_value, self.maximum, self.description)

    def increase(self, amount: int) -> 'BaseStat':
        new_current_value = min(self.maximum, self.current + amount)
        return BaseStat(self.name, new_current_value, self.maximum, self.description)



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