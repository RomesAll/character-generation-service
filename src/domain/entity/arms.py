from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, ConfigDict

class Equipment(ABC, BaseModel):
    name: str
    price: int
    max_durability: int
    current_durability: int
    peculiarities: object
    skills: list[object]

class Arms(Equipment):
    damage: int
    ignore_armor: int
    damage_armor: int
    max_endurance: int

class MeleeArms(Arms):
    pass

class RangedArms(Arms):
    range: int

class ShieldArms(Equipment):
    hand_protection: int
    shooting_protection: int