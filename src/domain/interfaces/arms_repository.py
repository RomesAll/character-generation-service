from abc import ABC, abstractmethod

class ArmsRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_all_melee(self):
        pass

    @abstractmethod
    def get_all_shield(self):
        pass

    @abstractmethod
    def get_all_ranged(self):
        pass
