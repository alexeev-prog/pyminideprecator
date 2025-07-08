import warnings

import pytest

from pyminideprecator import DeprecatedError, deprecate, set_current_version


@pytest.fixture(autouse=True)
def reset_config():
    set_current_version(None)


def test_function_warning():
    set_current_version('1.0.0')

    @deprecate('2.0.0', 'Test function')
    def test_func() -> int:
        return 42

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        assert test_func() == 42
        assert len(caught) == 1
        assert issubclass(caught[0].category, DeprecationWarning)
        assert 'Test function' in str(caught[0].message)


def test_class_warning():
    set_current_version('1.5.0')

    @deprecate('2.0.0', 'Test class')
    class TestClass:
        def method(self) -> str:
            return 'test'

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        obj = TestClass()
        assert obj.method() == 'test'
        assert len(caught) == 2


def test_error_after_remove_version():
    set_current_version('2.0.0')

    @deprecate('2.0.0', 'Removed function')
    def removed_func():
        pass

    with pytest.raises(DeprecatedError):
        removed_func()


def test_custom_error_version():
    set_current_version('1.9.0')

    @deprecate(remove_version='2.0.0', message='Early error', error_version='1.9.0')
    def early_error_func():
        pass

    with pytest.raises(DeprecatedError):
        early_error_func()


def test_date_based_deprecation():
    set_current_version('2023.06.15')

    @deprecate('2023.12.31', 'New year cleanup')
    def holiday_func():
        pass

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=DeprecationWarning)
        holiday_func()

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        holiday_func()
        assert len(caught) == 1
        assert 'New year cleanup' in str(caught[0].message)

    set_current_version('2024.01.01')
    with pytest.raises(DeprecatedError):
        holiday_func()


def test_docstring_modification():
    set_current_version('1.0.0')

    @deprecate('2.0.0', 'Doc test')
    def documented_func():
        """Original docs"""

    docs = str(documented_func.__doc__)
    assert 'DEPRECATED' in docs
    assert 'Doc test' in docs
    assert 'Original docs' in docs


def test_method_deprecation():
    set_current_version('1.0.0')

    class TestClass:
        @deprecate('2.0.0', 'Deprecated method')
        def test_method(self) -> int:
            return 42

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        obj = TestClass()
        assert obj.test_method() == 42
        assert len(caught) == 1
        assert 'Deprecated method' in str(caught[0].message)
