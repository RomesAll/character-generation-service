from pydantic import BaseModel, Field, ConfigDict, model_validator
from abc import ABC
from pathlib import Path

from src.domain.exceptions import CurrentGreaterMaximumException
from src.domain.value_object.enums import BodyPart


class Armor(ABC, BaseModel):
    """
    Абстрактный класс для хранения инф. о брони
    """
    model_config = ConfigDict(validate_assignment=True)
    name: str = Field(..., description="Название брони")
    endurance: int = Field(
        ..., description="Влияния на выносливость, чем выше, тем тяжелее броня"
    )
    max_durability: int = Field(
        ..., ge=0, le=320, description="Максимальная прочность брони"
    )
    current_durability: int = Field(..., ge=0, description="Текущая прочность брони")
    body_part: BodyPart
    image: Path

    @model_validator(mode="after")
    def validate_current_durability(self):
        """
        Проверка прочности брони
        :return:
        """
        if self.current_durability > self.max_durability:
            raise CurrentGreaterMaximumException(
                "Текущая прочность брони не может быть больше максимальной"
            )
        return self

    def take_damage(self, damage: int) -> None:
        """
        Получение урона для брони
        :param damage:
        :return:
        """
        self.current_durability = max(0, self.current_durability - damage)

    def repair(self, amount: int) -> None:
        """
        Починка брони
        :param amount:
        :return:
        """
        self.current_durability = min(
            self.max_durability, self.current_durability + amount
        )


class HeadArmor(Armor):
    """
    Хранение информации о брони головы
    """
    max_durability: int = Field(
        ..., ge=0, le=300, description="Максимальная прочность брони для головы"
    )
    price: int = Field(..., ge=15, le=4000, description="Цена брони для головы")


class BodyArmor(Armor):
    """
    Хранения информации о брони тела
    """
    max_durability: int = Field(
        ..., ge=0, le=320, description="Максимальная прочность брони для тела"
    )
    price: int = Field(..., ge=0, le=7000, description="Цена брони для тела")
