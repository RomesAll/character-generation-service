from typing import Callable
from collections import deque
import random, copy

from src.domain.entity.stats import GroupStat, StatEnum, MultiplierObject, BaseStat

def append_stat_history(func: Callable) -> Callable:
    def wrapper(self: 'StatsService | StatsService.GenerateCustomStat',
                *args, **kwargs) -> Callable:
        result = func(self, *args, **kwargs)
        if type(self) is StatsService:
            self.builder_stats.history_stats.appendleft(copy.deepcopy(self.builder_stats.stats_result))
        elif type(self) is StatsService.GenerateCustomStat:
            self.history_stats.append(copy.deepcopy(self.stats_result))
        return result
    return wrapper

class GenerateCustomStatMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        def create_method(stat_info: StatEnum):
            @append_stat_history
            def wrapper(self, *, current: int, maximum: int) -> 'StatsService.GenerateCustomStat':
                setattr(self.stats_result, stat_info.value[0], stat_info.value[1](
                    name=stat_info,
                    current=current,
                    maximum=maximum,
                ))
                # self.history_stats.appendleft(copy.deepcopy(self.stats_result))
                return self
            return wrapper
        for stat in StatEnum:
            attrs[stat.value[0]] = create_method(stat)
        print(attrs)
        return super().__new__(cls, name, bases, attrs)

class StatsService:
    def __init__(self):
        self.builder_stats = StatsService.GenerateCustomStat()

    @property
    def current_stats(self):
        return self.builder_stats.stats_result

    def generate_default_stats(self) -> GroupStat:
        (self.builder_stats.
         health(current=95,maximum=95).
         hand_skill(current=25,maximum=100))
        return self.current_stats

    def generate_random_stats(self, level: int = 0):
        _health = random.randint(40, 120)
        _hand_skill = random.randint(10, 70)
        (self.builder_stats.
         health(current=_health, maximum=_health).
         hand_skill(current=_hand_skill, maximum=100))
        for _ in range(level):
            self.level_up()
        return self.current_stats

    def _get_stat(self, stat: StatEnum):
        current_stat: BaseStat | None = getattr(self.builder_stats.stats_result, stat.value[0])
        return current_stat

    @append_stat_history
    def append_multipliers(self, stat: StatEnum, multiplier: MultiplierObject):
        if (current_stat := self._get_stat(stat)) is None:
            raise ValueError('Stat is None')
        current_stat.append_multipliers(multiplier)

    @append_stat_history
    def remove_multipliers(self, stat: StatEnum, multiplier: MultiplierObject):
        if (current_stat := self._get_stat(stat)) is None:
            raise ValueError('Stat is None')
        current_stat.remove_multipliers(multiplier)

    @append_stat_history
    def level_up(self):
        self.builder_stats.stats_result.level_up()

    class GenerateCustomStat(metaclass=GenerateCustomStatMeta):
        def __init__(self):
            self.stats_result: GroupStat = GroupStat()
            self.history_stats: deque[GroupStat] = deque(maxlen=100)

        def health(self, *, current: int, maximum: int) -> 'StatsService.GenerateCustomStat':
            raise NotImplementedError()

        def hand_skill(self, *, current: int, maximum: int) -> 'StatsService.GenerateCustomStat':
            raise NotImplementedError()