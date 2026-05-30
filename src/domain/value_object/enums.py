from enum import Enum

class EquipmentType(Enum):
    OND_HAND = 'одноручный предмет'
    TWO_HAND = 'двуручный предмет'

class BodyPart(Enum):
    HEAD = 'head'
    BODY = 'body'
    LEFT_HAND = 'left_hand'
    RIGHT_HAND = 'right_hand'

class Measurement(Enum):
    PERCENT = 'percent'
    UNITS = 'units'

class StatEnum(Enum):
    HEALTH = 'health'
    HAND_SKILL = 'hand_skill'
    BODY_ARMOR = 'body_armor'
    ACTION_POINT = 'action_point'
    BRAVERY = 'bravery'
    ENDURANCE = 'endurance'
    INITIATIVE = 'initiative'
    MELEE_DEFENSE = 'melee_defense'
    SHOOTING_PROTECTION = 'shooting_protection'
    DAMAGE = 'damage'
    VISIBILITY = 'visibility'
    MORAL = 'moral'
    SHOOTING_SKILL = 'shooting_skill'
    DAMAGE_ARMOR = 'damage_armor'
    HEAD_HIT_CHANCE = 'head_hit_chance'