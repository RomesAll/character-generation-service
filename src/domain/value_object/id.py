import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class CharacterID:
    value: uuid.UUID

    @classmethod
    def generate(cls):
        return cls(uuid.uuid4())

@dataclass(frozen=True)
class ImageID:
    value: uuid.UUID

    @classmethod
    def generate(cls):
        return cls(uuid.uuid4())