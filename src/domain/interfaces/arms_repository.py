from abc import ABC, abstractmethod
from src.domain.criteria.arms_criteria import ArmsCriteria

class ArmsRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_melee(self, filters: ArmsCriteria):
        pass

    @abstractmethod
    def get_all_shield(self, filters: ArmsCriteria):
        pass

    @abstractmethod
    def get_all_ranged(self, filters: ArmsCriteria):
        pass
