from pydantic import ValidationError
import pytest

from src.domain.entity.group_characteristics import GroupStat
from src.domain.entity.stats import Health
from contextlib import nullcontext
from src.domain.exceptions import CurrentGreaterMaximumException, LevelException
from src.domain.value_object import StatEnum, Measurement
from src.domain.value_object.perk import PerkMultiplier, Perk


@pytest.fixture(scope="module")
def create_group_stats():
    group_stats = GroupStat()
    return group_stats


class TestStats:
    @pytest.mark.parametrize(
        "current, maximum, expected",
        [
            (95, 95, nullcontext()),
            (-95, -95, pytest.raises(ValidationError)),
            (95, 20, pytest.raises(CurrentGreaterMaximumException)),
        ],
    )
    def test_health_create(self, current, maximum, expected):
        with expected:
            stat = Health(
                current=current,
                maximum=maximum,
            )
            assert stat.current == current
            assert stat.maximum == maximum


class TestGroupStat:
    def test_default_group_stats(self, create_group_stats):
        stat = create_group_stats.health
        assert stat.name == StatEnum.HEALTH
        assert 0 <= stat.current <= 200
        assert 0 <= stat.maximum <= 200

    def test_field_stat(self, create_group_stats):
        for stat in StatEnum:
            if stat.value != StatEnum.BODY_ARMOR.value:
                getattr(create_group_stats, stat.value)

    def test_get_copy(self, create_group_stats):
        copy = create_group_stats.get_copy()
        assert copy is not create_group_stats

    def test_change_group_stats(self, create_group_stats):
        group_stat = create_group_stats.get_copy()
        group_stat.with_health(
            current=11,
            maximum=11,
        ).with_action_point(
            current=5,
            maximum=5,
        ).with_moral(
            current=43,
            maximum=43,
        )
        assert group_stat.health.current == 11
        assert group_stat.action_point.current == 5
        assert group_stat.moral.current == 43

    def test_level_up(self, create_group_stats):
        group_stat = create_group_stats.get_copy()
        assert group_stat.level == 0
        group_stat.level_up()
        group_stat.level_up()
        group_stat.level_up()
        assert group_stat.level == 3
        with pytest.raises(LevelException):
            group_stat.level_up()
        new_maximum_health = group_stat.health.maximum
        old_maximum_health = create_group_stats.health.maximum
        assert new_maximum_health > old_maximum_health

    def test_copy_without_multiplier(self, create_group_stats):
        group_stat = create_group_stats.get_copy()
        group_stat.append_multipliers(PerkMultiplier(
                stat=StatEnum.HEALTH,
                amount=15,
                measurement=Measurement.UNITS,
            )
        )
        assert len(group_stat.health.multipliers) == 1
        new_copy = group_stat.get_copy_without_multiplier()
        assert len(new_copy.health.multipliers) == 0