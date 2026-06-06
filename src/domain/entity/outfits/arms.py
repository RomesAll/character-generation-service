from abc import ABC
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pathlib import Path

from src.domain.exceptions import CurrentGreaterMaximumException
from src.domain.value_object.enums import EquipmentType


class Equipment(ABC, BaseModel):
    """
    Абстрактный класс для хранения информации о предметах, которые можно подобрать
    """
    model_config = ConfigDict(validate_assignment=True)

    name: str = Field(..., frozen=True, description="Название оружия")
    type_equipment: EquipmentType = Field(
        ..., frozen=True, description="Тип оружия (одноручный, двуручный)"
    )
    price: int = Field(..., ge=0, description="Цена оружия")
    max_durability: int = Field(
        ..., ge=0, le=100, frozen=True, description="Максимальная прочность"
    )
    current_durability: int = Field(..., ge=0, le=100, description="Текущая прочность")
    peculiarities: object | None = Field(None, description="Особенности")
    image: Path

    @model_validator(mode="after")
    def validate_current_durability(self):
        if self.current_durability > self.max_durability:
            raise CurrentGreaterMaximumException("Текущая прочность оружия не может быть больше максимальной")
        return self

    def take_damage(self, damage: int) -> None:
        self.current_durability = max(0, self.current_durability - damage)

    def repair(self, amount: int) -> None:
        self.current_durability = min(
            self.max_durability, self.current_durability + amount
        )


class Arms(Equipment, ABC):
    """
    Хранения информации об оружии
    """
    damage: tuple[int, int] = Field(..., description="Урон оружия в диапазоне")
    ignore_armor: int = Field(..., ge=0, le=100, description="Игнорирование брони в %")
    damage_armor: int = Field(..., ge=0, le=100, description="Урон по броне в %")
    max_endurance: int = Field(..., description="Максимальная выносливость")

    @model_validator(mode="after")
    def validate_damage_difficulty(self):
        if self.damage[1] - self.damage[0] < 0:
            raise ValueError("Максимальный урон не может быть меньше минимального")
        return self


class MeleeArms(Arms):
    """
    Хранения информации о ближнем оружии
    """
    pass


class RangedArms(Arms):
    """
    Хранения информации о дальнем оружие
    """
    range: int = Field(..., ge=0, description="Дальность выстрела")


class ShieldArms(Equipment):
    """
    Хранения информации о щитах
    """
    melee_defense: int = Field(..., ge=1, description="Рукопашная защита")
    shooting_protection: int = Field(..., ge=1, description="Стрелковая защита")
