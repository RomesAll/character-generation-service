from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class IEffect(ABC):
    @abstractmethod
    def apply_effect(self, target):
        pass

    @abstractmethod
    def update_effect(self, target):
        pass

@dataclass
class PassiveEffect(IEffect, ABC):
    name: str
    description: str

@dataclass
class ActiveEffect(PassiveEffect, ABC):
    price_action_point: int
    duration: int

@dataclass
class ArmsEffect(ActiveEffect, ABC):
    pass

@dataclass
class RaceEffect(PassiveEffect, ABC):
    pass

@dataclass
class PerkEffect(PassiveEffect, ABC):
    pass

@dataclass
class CharacterFeatures(PassiveEffect, ABC):
    pass