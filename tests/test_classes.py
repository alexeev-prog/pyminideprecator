import warnings

import pytest

from pyminideprecator import DeprecatedError, deprecate, set_current_version
from pyminideprecator.deprecator import _generate_message


def test_deprecated_class_methods_warning():
    set_current_version("1.5.0")

    @deprecate("2.0.0", "Test class")
    class TestClass:
        @property
        @deprecate("2.0.0", "Test property")
        def method(self) -> str:
            return "test"

        @staticmethod
        @deprecate("2.0.0", "Test property")
        def static_method() -> str:
            return "test"

        @classmethod
        @deprecate("2.0.0", "Test property")
        def class_method(cls) -> str:
            return "test"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = TestClass()
        assert obj.method == "test"
        assert TestClass.static_method() == "test"
        assert obj.class_method() == "test"
        assert len(caught) == 5


def test_class_methods_warning():
    set_current_version("1.5.0")

    class TestClass:
        @property
        @deprecate("2.0.0", "Test property")
        def method(self) -> str:
            return "test"

        @staticmethod
        @deprecate("2.0.0", "Test property")
        def static_method() -> str:
            return "test"

        @classmethod
        @deprecate("2.0.0", "Test property")
        def class_method(cls) -> str:
            return "test"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = TestClass()
        assert obj.method == "test"
        assert obj.static_method() == "test"
        assert obj.class_method() == "test"
        assert len(caught) == 3


def test_class_methods_errors():
    set_current_version("2.5.0")

    class TestClass:
        @property
        @deprecate("2.0.0", "Test property")
        def method(self) -> str:
            return "test"

        @staticmethod
        @deprecate("2.0.0", "Test property")
        def static_method() -> str:
            return "test"

        @classmethod
        @deprecate("2.0.0", "Test property")
        def class_method(cls) -> str:
            return "test"

    obj = TestClass()

    with pytest.raises(DeprecatedError):
        assert obj.method == "test"
        assert obj.static_method() == "test"
        assert obj.class_method() == "test"
