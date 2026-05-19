from pydantic import BaseModel, Field, ConfigDict
from src.domain.value_object.equipment_type import EquipmentType
from src.domain.entity.arms import Equipment

class ArmsFastSlot(BaseModel):
    model_config = ConfigDict(
        extra='allow'
    )

    left_hand: object | None = Field(None, description='Слот под левую руку')
    right_hand: object | None = Field(None, description='Слот под правую руку')