from .hand_skill import HandSkill
from .health import Health
from src.domain.value_object.enums import Measurement, StatEnum
from .group_stats import GroupStat
from .base import BaseStat

MultiplierObject = tuple[int, Measurement]
MultipliersList = list[MultiplierObject]

MAPPING_STATS: dict = {
    StatEnum.HEALTH: Health,
    StatEnum.HAND_SKILL: HandSkill,
}

__all__ = [
    'HandSkill',
    'Health',
    'GroupStat',
    'BaseStat',
    'MAPPING_STATS',
    'MultiplierObject',
    'MultipliersList',
]