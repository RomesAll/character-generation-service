from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import copy, weakref

from src.domain.entity.fast_slot.decorators import change_character_stats
from src.domain.exceptions import BodyPartArmorException
from src.domain.value_object.enums import BodyPart
from src.domain.entity.outfits.armor import Armor, HeadArmor, BodyArmor
from src.domain.entity.group_characteristics.group_stats import GroupStat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entity.characters.character import Character


class ArmorFastSlot(BaseModel):
    """
    Хранит информацию об экипировки персонажа (голова, тело).
    Осуществляет управление установки и снятия экипировки и, в случае
    если есть ссылка на статы (GroupStat) персонажа, то меняет
    соответствующие статы (урон оружием, броня головы, броня тела) у
    персонажа
    """
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
        """
        Инициализация объекта, устанавливает ссылку на статы персонажа,
        для атрибута головы (head) и тела (body) устанавливается переданные
        объекты
        :param group_stat_ref: слабая ссылка на статы персонажа
        :param head: броня головы
        :param body: броня тела
        """
        super().__init__()
        self._group_stat_ref = group_stat_ref
        # атрибут head, body ссылается на вложенный класс ManageArmorItem для
        # получения доступа к методам для снятие и установки брони
        self.head = self.ManageArmorItem(
            body_part_name=BodyPart.HEAD, armor=head, outer=weakref.ref(self)
        )
        self.body = self.ManageArmorItem(
            body_part_name=BodyPart.BODY, armor=body, outer=weakref.ref(self)
        )

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

    def get_copy(self) -> "ArmorFastSlot":
        """
        Получение копии объекта ArmorFastSlot
        :return:
        """
        return copy.deepcopy(self)

    class ManageArmorItem(BaseModel):
        """
        Управляет установкой и снятием брони персонажа и
        изменения соответсвующий статов (броня головы, тела)
        """
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

        # хранит часть тела брони (голова, тело)
        body_part_name: BodyPart
        # объект брони
        armor: Armor | HeadArmor | BodyArmor | None = None
        # внешняя ссылка на ArmorFastSlot
        outer: weakref.ref["ArmorFastSlot"]

        @change_character_stats
        def equip(self, *, item: Armor | None = None) -> Armor | None:
            """
            Установка брони в слот персонажа
            :param item:
            :return:
            """
            if item and self.body_part_name != item.body_part:
                raise BodyPartArmorException(item, self.body_part_name)
            old_armor = self.armor
            self.armor = item
            return old_armor

        def unequip(self) -> Armor | None:
            """
            Снятия брони из слота персонажа
            :return:
            """
            return self.equip(item=None)
