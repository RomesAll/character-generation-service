from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.value_object.enums import StatEnum
    from src.domain.entity.stats import BaseStat, UnitStat, PercentStat

from src.domain.entity.stats import MAPPING_STATS

class BuilderStatMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        def crete_getter_method(stat_enum_object: 'StatEnum'):
            @property
            def wrapper(self):
                stat: 'BaseStat' = getattr(self, "_" + stat_enum_object.value)
                return stat
            return wrapper
        def create_setter_method(stat_enum_object: 'StatEnum', stat_object: type["UnitStat | PercentStat"]):
            def wrapper(self, *, current: int | tuple[int, int], maximum: int):
                stat: 'BaseStat' = getattr(self, "_" + stat_enum_object.value)
                new_object: 'BaseStat' = stat_object(current=current, maximum=maximum)
                setattr(self, "_" + stat_enum_object.value, new_object)
                for multiplier in stat.multipliers:
                    self.append_multipliers(multiplier)
                return self
            return wrapper
        for stat_enum, stat_obj in MAPPING_STATS.items():
            attrs[stat_enum.value] = crete_getter_method(stat_enum)
            attrs['with_' + stat_enum.value] = create_setter_method(stat_enum, stat_obj)
        return super().__new__(cls, name, bases, attrs)