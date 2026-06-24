import random
from src.domain.entity.characters import Character
from src.domain.entity.outfits import HeadArmor, Equipment
from src.domain.entity.stats.stats import BodyArmor
from pathlib import Path

from src.domain.interfaces.armor_repository import ArmorRepository
from src.domain.interfaces.arms_repository import ArmsRepository
from src.domain.interfaces.character_repository import CharacterRepository
from src.domain.interfaces.image_repository import ImageRepository
from src.domain.interfaces.name_generator import NameGenerator
from src.domain.value_object.id import CharacterID, ImageID


class CharacterGenerationService:
    def __init__(self,
                 character_repo: CharacterRepository,
                 image_repo: ImageRepository,
                 name_generator: NameGenerator,
                 armor_repo: ArmorRepository,
                 arms_repo: ArmsRepository) -> None:
        self._character_repo = character_repo
        self._image_repo = image_repo
        self._name_generator = name_generator
        self._armor_repo = armor_repo
        self._arms_repo = arms_repo

    def generate(
            self,
            image: ImageID,
            head: HeadArmor,
            body: BodyArmor,
            left_hand: Equipment,
            right_hand: Equipment,
            name: str | None = None,
    ) -> Character:
        if name is None:
            name = self._name_generator.generate()
        character_id = self._get_unique_id()
        image = self._image_repo.get(image)
        character = Character(
            character_id=character_id,
            name=name,
            head=head,
            body=body,
            left_hand=left_hand,
            right_hand=right_hand,
            image=image,
        )
        self._character_repo.save(character)
        return character

    def random_generate(self) -> Character:
        character_id = self._get_unique_id()
        name = self._name_generator.generate()
        image = random.choice(self._image_repo.get_all())
        head = random.choice(self._armor_repo.get_all_head())
        body = random.choice(self._armor_repo.get_all_body())
        left_hand = random.choice(self._arms_repo.get_all())
        right_hand = random.choice(self._arms_repo.get_all())
        character = Character(
            character_id=character_id,
            name=name,
            image=image,
            head=head,
            body=body,
            left_hand=left_hand,
            right_hand=right_hand,
        )
        self._character_repo.save(character)
        return character

    def _get_unique_id(self):
        counter = 0
        while character_id := CharacterID.generate():
            if not self._character_repo.get(character_id):
                break
            if counter > 10:
                raise RuntimeError('Слишком много попыток создать uuid для персонажа, дублированность uuid')
            counter += 1
        return character_id