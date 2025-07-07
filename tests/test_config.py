import pytest
from pyminideprecator.exc import DeprecatedError
from pyminideprecator.config import get_current_version, set_current_version
from pyminideprecator.version import Version


def test_set_version_with_string():
    set_current_version("1.2.3")
    v = get_current_version()
    assert v is not None
    assert v.parts == (1, 2, 3)


def test_global_version_with_imports(monkeypatch):
    import global_version_module
    set_current_version("3.0.0", set_global=True)

    with pytest.raises(DeprecatedError):
        global_version_module.test_global()

    set_current_version(None, set_global=True)


def test_global_class_version_with_imports(monkeypatch):
    import global_version_module
    set_current_version(Version("3.0.0"), set_global=True)

    with pytest.raises(DeprecatedError):
        global_version_module.test_global()

    set_current_version(None, set_global=True)


def test_set_version_with_version_object():
    ver = Version("2023.12.31")
    set_current_version(ver)
    assert get_current_version() == ver


def test_set_version_with_none():
    set_current_version(None)
    assert get_current_version() is None


def test_get_version_when_not_set():
    set_current_version(None)
    assert get_current_version() is None
