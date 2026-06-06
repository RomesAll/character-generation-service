from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from typing import TYPE_CHECKING
import copy, weakref

from src.domain.entity.fast_slot.decorators import change_character_stats
from src.domain.entity.group_characteristics.group_stats import GroupStat
from src.domain.value_object.enums import EquipmentType, BodyPart
from src.domain.entity.outfits.arms import Equipment

if TYPE_CHECKING:
    from src.domain.entity.characters.character import Character


class ArmsFastSlot(BaseModel):
    """
    Хранит информацию об экипировки персонажа (левая рука, правая рука).
    Осуществляет управление установки и снятия экипировки и, в случае
    если есть ссылка на статы (GroupStat) персонажа, то меняет
    соответствующие статы (урон оружием, броня головы, броня тела) у
    персонажа
    """
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    left_hand: "ArmsFastSlot.ManageHandItem | None" = Field(
        None, description="Слот под левую руку"
    )
    right_hand: "ArmsFastSlot.ManageHandItem | None" = Field(
        None, description="Слот под правую руку"
    )
    _group_stat_ref: weakref.ref["GroupStat"] | None = PrivateAttr(None)

    def __init__(
        self,
        group_stat_ref: weakref.ref["Character"] | None = None,
        left_hand: Equipment | None = None,
        right_hand: Equipment | None = None,
    ):
        """
        Инициализация объекта, устанавливает ссылку на статы персонажа,
        для атрибута left_hand и тела right_hand устанавливается переданные
        объекты
        :param group_stat_ref: слабая ссылка на статы персонажа
        :param left_hand: предмет в левой руке
        :param right_hand: предмет в правой руке
        """
        super().__init__()
        self._character = group_stat_ref
        # атрибут left_hand, right_hand ссылается на вложенный класс ManageHandItem для
        # получения доступа к методам для снятие и установки оружия, предмета
        self.left_hand = self.ManageHandItem(
            hand_name=BodyPart.LEFT_HAND,
            item_in_hand=left_hand,
            outer=weakref.ref(self),
        )
        self.right_hand = self.ManageHandItem(
            hand_name=BodyPart.RIGHT_HAND,
            item_in_hand=right_hand,
            outer=weakref.ref(self),
        )
        self.left_hand.other_hand = self.right_hand
        self.right_hand.other_hand = self.left_hand

    @property
    def group_stat(self):
        """
        Получения mutable объекта группы статов GroupStat
        :return:
        """
        return self._group_stat_ref() if self._group_stat_ref else None

    @group_stat.setter
    def group_stat(self, value: weakref.ref["GroupStat"]):
        """
        Установка группы статов
        :param value:
        :return:
        """
        self._group_stat_ref = value

    def get_copy(self) -> "ArmsFastSlot":
        """
        Получение копии объекта ArmsFastSlot
        :return:
        """
        return copy.deepcopy(self)

    class ManageHandItem(BaseModel):
        """
        Управляет установкой и снятием предмета с левой, правой руки и
        изменения соответсвующий статов (броня головы, тела)
        """
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

        # хранит часть тела для предмета (левая, правая рука)
        hand_name: BodyPart
        # объект предмета
        item_in_hand: Equipment | None = None
        # другая рука (нужная для двуручных предметов)
        other_hand: "ArmsFastSlot.ManageHandItem | None" = Field(None, repr=False)
        # # внешняя ссылка на ArmorFastSlot
        outer: weakref.ref["ArmsFastSlot"]

        @change_character_stats
        def equip(
            self, *, item: Equipment | None = None
        ) -> Equipment | tuple[Equipment, ...] | tuple[None, ...] | None:
            """
            Установка предмета в слот персонажа
            :param item:
            :return:
            """
            old_item_self: Equipment = self.item_in_hand
            old_item_other: Equipment = self.other_hand.item_in_hand
            if item and item.type_equipment == EquipmentType.TWO_HAND:
                self.item_in_hand = item
                self.other_hand.item_in_hand = item
                if id(old_item_self) != id(old_item_other):
                    return old_item_self, old_item_other
                return old_item_self
            if old_item_self and old_item_self.type_equipment == EquipmentType.TWO_HAND:
                self.other_hand.item_in_hand = None
            self.item_in_hand = item
            return old_item_self

        def unequip(
            self,
        ) -> Equipment | tuple[Equipment, ...] | tuple[None, ...] | None:
            """
            Снятия предмета из слота персонажа
            :return:
            """
            return self.equip(item=None)
