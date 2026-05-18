from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, ConfigDict

class Armor(ABC, BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str = Field(..., description='Название брони')
    endurance: int = Field(..., description='Влияния на выносливость, '
                                             'чем выше, тем тяжелее броня')
    durability: int = Field(..., ge=0, le=320, description='Прочность брони')

    @abstractmethod
    def take_damage(self, damage: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def repair(self, amount: int) -> None:
        raise NotImplementedError()

class HeadArmor(Armor):
    durability: int = Field(...,ge=0, le=300, description='Прочность брони для головы')
    price: int = Field(..., ge=15, le=4000, description='Цена брони для головы')

class BodyArmor(Armor):
    durability: int = Field(..., ge=0, le=320, description='Прочность брони для тела')
    price: int = Field(..., ge=0, le=7000, description='Цена брони для тела')

class UniqueHeadArmor(HeadArmor):
    pass

class UniqueBodyArmor(BodyArmor):
    pass