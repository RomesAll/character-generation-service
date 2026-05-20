from pydantic import BaseModel
from src.domain.entity.group_stat import GroupStat
from src.domain.value_object.effect import PerkEffect, ActiveEffect, CharacterFeatures
from src.domain.entity.fast_slot import ArmsFastSlot
from src.domain.entity.arms import *
from src.domain.entity.armor import *
import weakref

class Character(BaseModel):
    first_name: str
    second_name: str

    stat: GroupStat
    perks: list[PerkEffect]
    active_effects: list[ActiveEffect]
    character_features: list[CharacterFeatures]

    head: HeadArmor
    body: BodyArmor

    left_hand: weakref.ref
    right_hand: weakref.ref

    arms_slot: list[ArmsFastSlot]
    inventory: list[object]

