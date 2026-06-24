from abc import ABC, abstractmethod

class CharacterRandGenerator(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def join(self):
        pass

    @abstractmethod
    def terminate(self):
        pass


