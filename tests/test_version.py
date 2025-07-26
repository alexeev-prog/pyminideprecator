from datetime import date

import pytest

from pyminideprecator import Version


def test_equals_versions():
    v1 = Version("1.2.3")
    v2 = Version("1.2.3")
    v3 = Version("1.2.4")
    assert v1 == v2
    assert v1 != v3
    assert v2 != v3

    assert hash(v1) == hash(v2)
    assert hash(v1) != hash(v3)
    assert hash(v2) != hash(v3)


def test_semantic_version():
    v = Version("1.2.3")
    assert not v.is_date
    assert v.parts == (1, 2, 3)
    assert repr(v) == "Version('1.2.3')"


def test_date_version():
    v = Version("2025.12.31")
    assert v.is_date
    assert v.date == date(2025, 12, 31)
    assert repr(v) == "Version('2025.12.31')"


def test_invalid_version():
    with pytest.raises(ValueError, match="Invalid version format"):
        Version("invalid")


def test_semantic_comparison():
    v1 = Version("1.2.3")
    v2 = Version("1.2.4")
    v3 = Version("1.2.3")

    assert v1 < v2
    assert v1 <= v3
    assert v2 > v1
    assert v3 >= v1
    assert not (v1 > v2)
    assert not (v2 < v1)


def test_date_comparison():
    v1 = Version("2025.01.01")
    v2 = Version("2025.01.02")
    v3 = Version("2025.01.01")

    assert v1 < v2
    assert v1 <= v3
    assert v2 > v1
    assert v3 >= v1
    assert not (v1 > v2)
    assert not (v2 < v1)


def test_mixed_comparison():
    v1 = Version("1.2.3")
    v2 = Version("2025.01.01")
    x = False

    with pytest.raises(TypeError, match="Cannot compare different version types"):
        x = v1 < v2

    with pytest.raises(TypeError, match="Cannot compare different version types"):
        x = v1 > v2

    assert not x


def test_equal_comparison():
    v1 = Version("1.2.3")
    v2 = Version("1.2.3")
    assert not (v1 < v2)
    assert not (v1 > v2)
