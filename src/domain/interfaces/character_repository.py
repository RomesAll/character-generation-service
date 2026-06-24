from abc import abstractmethod, ABC
from src.domain.entity.characters import Character
from src.domain.value_object.id import CharacterID


class CharacterRepository(ABC):
    @abstractmethod
    def get(self, id: CharacterID):
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