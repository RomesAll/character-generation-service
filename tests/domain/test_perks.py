from contextlib import nullcontext
from copy import copy
import weakref, pytest

from src.domain.entity.group_characteristics import GroupStat, GroupPerk
from src.domain.exceptions import (
    StatEnumTypeException,
    NamePerkException,
    PerkMultiplierException,
)
from src.domain.value_object import Measurement, StatEnum
from src.domain.value_object.perk import Perk, PerkMultiplier


@pytest.fixture(scope="module")
def perk_multipliers():
    perk_multiplier1 = PerkMultiplier(
        stat=StatEnum.HEALTH, amount=10, measurement=Measurement.UNITS
    )
    perk_multiplier2 = PerkMultiplier(
        stat=StatEnum.MELEE_DEFENSE, amount=2, measurement=Measurement.PERCENT
    )
    perk_multiplier3 = PerkMultiplier(
        stat=StatEnum.MORAL, amount=77, measurement=Measurement.UNITS
    )
    return perk_multiplier1, perk_multiplier2, perk_multiplier3


@pytest.fixture(scope="module")
def perk(perk_multipliers):
    perk = Perk(
        name="perk1",
        multipliers=(perk_multipliers[0], perk_multipliers[1], perk_multipliers[2]),
    )
    return perk


@pytest.fixture(scope="function")
def group_perk_stat(perk_multipliers):
    group_stats = GroupStat()
    group_perks = GroupPerk(group_stats=weakref.ref(group_stats))
    group_perks.add(name_perk="perk1", multipliers=perk_multipliers)
    return group_perks, group_stats


class TestPerkMultiplier:
    def test_default_create(self, perk_multipliers):
        assert isinstance(perk_multipliers[0], PerkMultiplier)
        assert perk_multipliers[0].owner is None
        assert perk_multipliers[0].amount == 10
        assert perk_multipliers[0].measurement is Measurement.UNITS
        assert perk_multipliers[0].stat is StatEnum.HEALTH

    def test_refresh(self, perk_multipliers):
        with pytest.raises(AttributeError):
            setattr(perk_multipliers[0], "amount", 11)
        assert perk_multipliers[0].amount == 10

    def test_copy(self, perk_multipliers):
        new_perk_multiplier = copy(perk_multipliers[0])
        assert id(perk_multipliers[0]) != id(new_perk_multiplier)

    def test_eq(self, perk_multipliers):
        new_perk_multiplier = copy(perk_multipliers[0])
        assert perk_multipliers[0] == new_perk_multiplier

    def test_not_eq(self, perk_multipliers):
        new_perk_multiplier = PerkMultiplier(
            stat=StatEnum.HEALTH, amount=20, measurement=Measurement.UNITS
        )
        assert perk_multipliers[0] != new_perk_multiplier

    @pytest.mark.parametrize(
        "stat, amount, measurement, expected",
        [
            (StatEnum.HEALTH, 10, Measurement.UNITS, nullcontext()),
            (StatEnum.ENDURANCE, 10, Measurement.UNITS, nullcontext()),
            (None, 10, Measurement.UNITS, pytest.raises(StatEnumTypeException)),
        ],
    )
    def test_exception(self, stat, amount, measurement, expected):
        with expected:
            PerkMultiplier(stat=stat, amount=amount, measurement=measurement)


class TestPerk:
    def test_create(self):
        perk = Perk(name="perk1")
        assert perk.name == "perk1"
        assert len(perk.multipliers) == 0

    def test_name_perk_exception(self):
        with pytest.raises(NamePerkException):
            Perk(name="p")

    def test_multiplier_perk_exception(self):
        with pytest.raises(PerkMultiplierException):
            Perk(name="perk1", multipliers=[None, None])

    def test_group_perk(self):
        group_stats = GroupStat()
        group_perks = GroupPerk(group_stats=weakref.ref(group_stats))
        assert group_perks.group_stats == group_stats

    def test_group_perk_add(self, perk_multipliers):
        group_stats = GroupStat()
        group_perks = GroupPerk(group_stats=weakref.ref(group_stats))
        group_perks.add(name_perk="perk1", multipliers=perk_multipliers)
        assert group_perks.group_stats == group_stats
        assert group_stats.health.maximum == 10
        assert group_stats.melee_defense.maximum == 0
        assert group_stats.moral.maximum == 77

    def test_refresh_multiplier(self, group_perk_stat):
        group_perks, group_stats = group_perk_stat
        new_group_stats = GroupStat()
        group_perks.group_stats = weakref.ref(new_group_stats)
        group_perks.refresh_all_multiplier()
        assert group_perks.group_stats == group_stats
        assert group_stats.health.maximum == 10
        assert group_stats.melee_defense.maximum == 0
        assert group_stats.moral.maximum == 77

    def test_remove_perk(self, group_perk_stat):
        group_perks, group_stats = group_perk_stat
        perks: list[Perk] = group_perks.perks
        group_perks.remove(name_perk=perks[0].name)
        assert group_stats.health.maximum == 0
        assert group_stats.melee_defense.maximum == 0
        assert group_stats.moral.maximum == 0
