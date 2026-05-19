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
class Health(BaseStat):
    pass

@dataclass(frozen=True)
class ArmorHead(BaseStat):
    pass

@dataclass(frozen=True)
class ArmorBody(BaseStat):
    pass

@dataclass(frozen=True)
class ActionPoint(BaseStat):
    pass

@dataclass(frozen=True)
class Endurance(BaseStat):
    pass

@dataclass(frozen=True)
class Moral(BaseStat):
    pass

@dataclass(frozen=True)
class Courage(BaseStat):
    pass

@dataclass(frozen=True)
class HandScourge(BaseStat):
    pass

@dataclass(frozen=True)
class ShootingSkill(BaseStat):
    pass

@dataclass(frozen=True)
class HandProtection(BaseStat):
    pass

@dataclass(frozen=True)
class ShootingProtection(BaseStat):
    pass

@dataclass(frozen=True)
class Damage(BaseStat):
    pass

@dataclass(frozen=True)
class DamageArmor(BaseStat):
    pass

@dataclass(frozen=True)
class HeadHitChance(BaseStat):
    pass

@dataclass(frozen=True)
class Visibility(BaseStat):
    pass