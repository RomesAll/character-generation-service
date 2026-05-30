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