import uuid
from abc import ABC, abstractmethod
from pathlib import Path

class ImageRepository(ABC):
    @abstractmethod
    def get(self, id: uuid.UUID):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, image: Path):
        pass
