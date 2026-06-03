from copy import copy

from src.domain.exceptions import InvalidReferenceException, StatEnumTypeException, NamePerkException, \
    PerkMultiplierException
from src.domain.value_object import Measurement, StatEnum
from src.domain.value_object.perk import Perk, PerkMultiplier
from contextlib import nullcontext
import pytest, weakref

@pytest.fixture(scope='module')
def default_perk_and_multiplier():
    perk = Perk(name='perk1')
    perk_multiplier = PerkMultiplier(
        owner=weakref.ref(perk),
        stat=StatEnum.HEALTH,
        amount=10,
        measurement=Measurement.UNITS
    )
    return perk, perk_multiplier

class TestPerkMultiplier:
    def test_default_create(self, default_perk_and_multiplier):
        perk, perk_multiplier = default_perk_and_multiplier
        assert isinstance(perk_multiplier, PerkMultiplier)
        assert perk_multiplier.owner() is perk
        assert perk_multiplier.amount == 10
        assert perk_multiplier.measurement is Measurement.UNITS
        assert perk_multiplier.stat is StatEnum.HEALTH

    def test_refresh(self, default_perk_and_multiplier):
        _, perk_multiplier = default_perk_and_multiplier
        with pytest.raises(AttributeError):
            setattr(perk_multiplier, 'amount', 11)
        assert perk_multiplier.amount == 10

    def test_copy(self, default_perk_and_multiplier):
        _, perk_multiplier = default_perk_and_multiplier
        new_perk_multiplier = copy(perk_multiplier)
        assert id(perk_multiplier) != id(new_perk_multiplier)

    def test_eq(self, default_perk_and_multiplier):
        _, perk_multiplier = default_perk_and_multiplier
        new_perk_multiplier = copy(perk_multiplier)
        assert perk_multiplier == new_perk_multiplier

    def test_not_eq(self, default_perk_and_multiplier):
        _, perk_multiplier = default_perk_and_multiplier
        new_perk = Perk(name='perk2')
        new_perk_multiplier = PerkMultiplier(
            owner=weakref.ref(new_perk),
            stat=StatEnum.HEALTH,
            amount=10,
            measurement=Measurement.UNITS
        )
        assert perk_multiplier != new_perk_multiplier

    @pytest.mark.parametrize("owner, stat, amount, measurement, expected",
                             [
                                 (None, StatEnum.HEALTH, 10, Measurement.UNITS, pytest.raises(InvalidReferenceException)),
                                 (Perk(name='perk1'), StatEnum.HEALTH, 10, Measurement.UNITS, nullcontext()),
                                 (Perk(name='perk1'), None, 10, Measurement.UNITS, pytest.raises(StatEnumTypeException))
                             ])
    def test_exception(self, owner, stat, amount, measurement, expected):
        with expected:
            PerkMultiplier(
                owner=weakref.ref(owner) if owner else None,
                stat=stat,
                amount=amount,
                measurement=measurement
            )

class TestPerk:
    def test_create(self):
        perk = Perk(name='perk1')
        assert perk.name == 'perk1'
        assert len(perk.multipliers) == 0

    def test_name_perk_exception(self):
        with pytest.raises(NamePerkException):
            Perk(name='p')

    def test_multiplier_perk_exception(self):
        with pytest.raises(PerkMultiplierException):
            Perk(name='perk1', multipliers=[None, None])