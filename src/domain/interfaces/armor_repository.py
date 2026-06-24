from abc import ABC, abstractmethod

class ArmorRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_all_head(self):
        pass

    @abstractmethod
    def get_all_body(self):
        pass