from abc import abstractmethod, ABC
from src.domain.entity.characters import Character
import uuid

class CharacterRepository(ABC):
    @abstractmethod
    def get(self, id: uuid.UUID):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, character: Character):
        pass

    @abstractmethod
    def find_by_name(self, name: str):
        pass