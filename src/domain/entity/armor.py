from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, ConfigDict, model_validator

class Armor(ABC, BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str = Field(..., description='Название брони')
    endurance: int = Field(..., description='Влияния на выносливость, '
                                             'чем выше, тем тяжелее броня')
    max_durability: int = Field(..., ge=0, le=320, description='Максимальная прочность брони')
    current_durability: int = Field(..., ge=0, description='Текущая прочность брони')

    @model_validator(mode='after')
    def validate_current_durability(self):
        if self.current_durability > self.max_durability:
            raise ValueError('Текущая прочность брони не может быть больше максимальной')
        return self

    def take_damage(self, damage: int) -> None:
        self.current_durability = max(0, self.current_durability - damage)

    def repair(self, amount: int) -> None:
        self.current_durability = min(self.max_durability, self.current_durability + amount)

class HeadArmor(Armor):
    max_durability: int = Field(...,ge=0, le=300, description='Максимальная прочность брони для головы')
    price: int = Field(..., ge=15, le=4000, description='Цена брони для головы')

class BodyArmor(Armor):
    max_durability: int = Field(..., ge=0, le=320, description='Максимальная прочность брони для тела')
    price: int = Field(..., ge=0, le=7000, description='Цена брони для тела')

class UniqueHeadArmor(HeadArmor):
    pass

class UniqueBodyArmor(BodyArmor):
    pass