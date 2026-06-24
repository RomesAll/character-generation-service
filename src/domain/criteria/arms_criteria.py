from dataclasses import dataclass
from src.domain.value_object import EquipmentType

@dataclass(frozen=True)
class ArmsCriteria:
    name: str | None = None
    type_equipment: EquipmentType | None = None
