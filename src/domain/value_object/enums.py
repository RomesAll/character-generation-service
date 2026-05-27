from enum import Enum
from typing import TYPE_CHECKING

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