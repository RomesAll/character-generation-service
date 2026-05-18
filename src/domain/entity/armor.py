from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Armor(ABC):
    _name: str
    _durability: int
    _endurance: int

@dataclass
class HeadArmor(Armor):
    armor_head: int

@dataclass
class BodyArmor(Armor):
    armor_body: int

@dataclass
class UniqueHeadArmor(HeadArmor):
    pass

@dataclass
class UniqueBodyArmor(BodyArmor):
    pass

