import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.value_object.id import ImageID


class ImageRepository(ABC):
    @abstractmethod
    def get(self, id: ImageID):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, image: Path):
        pass
