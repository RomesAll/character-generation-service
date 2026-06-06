from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import copy, weakref

from src.domain.entity.fast_slot.decorators import change_armor_stats
from src.domain.exceptions import BodyPartArmorException
from src.domain.value_object.enums import BodyPart
from src.domain.entity.outfits.armor import Armor, HeadArmor, BodyArmor
from src.domain.entity.group_characteristics.group_stats import GroupStat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.characters.character import Character


class ArmorFastSlot(BaseModel):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    head: "ArmorFastSlot.ManageArmorItem | None" = Field(
        None, description="Слот для головы"
    )
    body: "ArmorFastSlot.ManageArmorItem | None" = Field(
        None, description="Слот для тела"
    )
    _group_stat_ref: weakref.ref["GroupStat"] | None = PrivateAttr(None)

    def __init__(
        self,
        group_stat_ref: weakref.ref["Character"] | None = None,
        head: HeadArmor | None = None,
        body: BodyArmor | None = None,
    ):
        super().__init__()
        self._group_stat_ref = group_stat_ref
        self.head = self.ManageArmorItem(
            body_part_name=BodyPart.HEAD, armor=head, outer=weakref.ref(self)
        )
        self.body = self.ManageArmorItem(
            body_part_name=BodyPart.BODY, armor=body, outer=weakref.ref(self)
        )

    @property
    def group_stat(self):
        return self._group_stat_ref() if self._group_stat_ref else None

    @group_stat.setter
    def group_stat(self, value: weakref.ref["GroupStat"]):
        self._group_stat_ref = value

    def get_copy(self) -> "ArmorFastSlot":
        return copy.deepcopy(self)

    class ManageArmorItem(BaseModel):
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

        body_part_name: BodyPart
        armor: Armor | HeadArmor | BodyArmor | None = None
        outer: weakref.ref["ArmorFastSlot"]

        @change_armor_stats
        def equip(self, *, item: Armor | None = None) -> Armor | None:
            if item and self.body_part_name != item.body_part:
                raise BodyPartArmorException(item, self.body_part_name)
            old_armor = self.armor
            self.armor = item
            return old_armor

        def unequip(self) -> Armor | None:
            return self.equip(item=None)
