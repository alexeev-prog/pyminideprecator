import asyncio
import warnings

import pytest

from pyminideprecator import (
    DeprecatedError,
    deprecate,
    scoped_version,
    set_current_version,
)
from pyminideprecator.deprecator import _generate_message


def test_async_function_warning():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Test async function")
    async def async_test_func() -> int:
        await asyncio.sleep(0.01)
        return 42

    async def run_test():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = await async_test_func()
            assert result == 42
            assert len(caught) == 1
            assert issubclass(caught[0].category, DeprecationWarning)
            assert "Test async function" in str(caught[0].message)

    asyncio.run(run_test())


def test_async_function_error():
    set_current_version("2.0.0")

    @deprecate("2.0.0", "Removed async function")
    async def async_removed_func() -> str:
        await asyncio.sleep(0.01)
        return "should not run"

    async def run_test():
        with pytest.raises(DeprecatedError):
            await async_removed_func()

    asyncio.run(run_test())


def test_async_method_deprecation():
    set_current_version("1.0.0")

    class AsyncTestClass:
        @deprecate("2.0.0", "Deprecated async method")
        async def async_method(self) -> int:
            await asyncio.sleep(0.01)
            return 42

    async def run_test():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            obj = AsyncTestClass()
            result = await obj.async_method()
            assert result == 42
            assert len(caught) == 1
            assert "Deprecated async method" in str(caught[0].message)

    asyncio.run(run_test())


def test_mixed_async_sync_deprecation():
    set_current_version("1.0.0")

    class MixedTestClass:
        @deprecate("2.0.0", "Sync method")
        def sync_method(self) -> int:
            return 42

        @deprecate("2.0.0", "Async method")
        async def async_method(self) -> int:
            await asyncio.sleep(0.01)
            return 24

    async def run_test():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            obj = MixedTestClass()

            # Test sync method
            assert obj.sync_method() == 42

            # Test async method
            assert await obj.async_method() == 24

            assert len(caught) == 2

    asyncio.run(run_test())


@pytest.fixture(autouse=True)
def reset_config():
    set_current_version(None)


def test_function_warning():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Test function")
    def test_func() -> int:
        return 42

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert test_func() == 42
        assert len(caught) == 1
        assert issubclass(caught[0].category, DeprecationWarning)
        assert "Test function" in str(caught[0].message)


def test_class_warning():
    set_current_version("1.5.0")

    @deprecate("2.0.0", "Test class")
    class TestClass:
        def method(self) -> str:
            return "test"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = TestClass()
        assert obj.method() == "test"
        assert len(caught) == 2


def test_error_after_remove_version():
    set_current_version("2.0.0")

    @deprecate("2.0.0", "Removed function")
    def removed_func():
        pass

    with pytest.raises(DeprecatedError):
        removed_func()


def test_scoped_version():
    set_current_version("2.0.1")

    @deprecate("2.0.0", "Removed function")
    def removed_func():
        pass

    with pytest.raises(DeprecatedError):
        removed_func()

    with warnings.catch_warnings(record=True) as caught:
        with scoped_version("1.9.9"):
            removed_func()
            assert len(caught) == 1


def test_custom_error_version():
    set_current_version("1.9.0")

    @deprecate(remove_version="2.0.0", message="Early error", error_version="1.9.0")
    def early_error_func():
        pass

    with pytest.raises(DeprecatedError):
        early_error_func()


def test_date_based_deprecation():
    set_current_version("2025.06.15")

    @deprecate("2025.12.31", "New year cleanup")
    def holiday_func():
        pass

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        holiday_func()
        assert len(caught) == 1
        assert "New year cleanup" in str(caught[0].message)

    set_current_version("2026.01.01")
    with pytest.raises(DeprecatedError):
        holiday_func()


def test_docstring_modification():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Doc test")
    def documented_func():
        """Original docs"""

    docs = str(documented_func.__doc__)
    assert "DEPRECATED" in docs
    assert "Doc test" in docs
    assert "Original docs" in docs


def test_method_deprecation():
    set_current_version("1.0.0")

    class TestClass:
        @deprecate("2.0.0", "Deprecated method")
        def test_method(self) -> int:
            return 42

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = TestClass()
        assert obj.test_method() == 42
        assert len(caught) == 1
        assert "Deprecated method" in str(caught[0].message)


def test_without_since_instead():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Simple message")
    def simple_func():
        pass

    with warnings.catch_warnings(record=True) as caught:
        simple_func()
        assert "Simple message" in str(caught[0].message)
        assert "since" not in str(caught[0].message)
        assert "instead" not in str(caught[0].message)


def test_without_current_version():
    set_current_version(None)

    @deprecate("2.0.0", "No version set")
    def versionless_func():
        pass

    with warnings.catch_warnings(record=True) as caught:
        versionless_func()
        assert len(caught) == 1


def test_custom_warning_category():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Future warning", category=FutureWarning)
    def future_func():
        pass

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        future_func()
        assert issubclass(caught[0].category, FutureWarning)


def test_class_docstring():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Class doc test")
    class DocumentedClass:
        """Original class docs"""

    docs = str(DocumentedClass.__doc__)
    assert "DEPRECATED CLASS" in docs
    assert "Class doc test" in docs
    assert "Original class docs" in docs


def test_error_before_remove_version():
    set_current_version("1.9.0")

    @deprecate(
        remove_version="2.0.0",
        message="Test error before remove",
        error_version="1.9.0",
    )
    def error_func():
        return "should not run"

    with pytest.raises(DeprecatedError):
        error_func()

    set_current_version("1.8.9")

    with warnings.catch_warnings(record=True):
        result = error_func()

    assert result == "should not run"


def test_class_without_methods():
    set_current_version("1.0.0")

    @deprecate("2.0.0", "Empty class")
    class EmptyClass:
        pass

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = EmptyClass()
        assert len(caught) == 1


def test_static_method_deprecation():
    set_current_version("1.0.0")

    class TestClass:
        @deprecate("2.0.0", "Static method")
        @staticmethod
        def static_method() -> int:
            return 42

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert TestClass.static_method() == 42
        assert len(caught) == 1
        assert "Static method" in str(caught[0].message)


def test_property_deprecation():
    set_current_version("1.0.0")

    class TestClass:
        @property
        @deprecate("2.0.0", "Deprecated property")
        def test_prop(self) -> str:
            return "value"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        obj = TestClass()
        assert obj.test_prop == "value"
        assert len(caught) == 1
        assert "Deprecated property" in str(caught[0].message)


def test_error_version_different_from_remove():
    set_current_version("1.5.0")

    @deprecate(
        remove_version="2.0.0",
        message="Test different error version",
        error_version="1.5.0",
    )
    def error_func():
        return "should error"

    with pytest.raises(DeprecatedError):
        error_func()

    set_current_version("1.4.9")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert error_func() == "should error"


def test__generate_message():
    msg = _generate_message("test.", "0.1.0")
    assert msg == "test. Will be removed in 0.1.0."

    msg2 = _generate_message("test.", "0.1.0", "0.0.5")
    assert msg2 == "Deprecated since 0.0.5. test. Will be removed in 0.1.0."

    msg3 = _generate_message("test.", "0.1.0", instead="msg0")
    assert msg3 == "test. Use msg0 instead. Will be removed in 0.1.0."


def test__decorate_class():
    set_current_version("3.0.0")

    @deprecate(remove_version="2.0.0", message="Example class is deprecated")
    class Example:
        def __init__(self, a: int = 1):
            self.a = a

        def square(self) -> int:
            return self.a * 2

    with pytest.raises(DeprecatedError):
        example = Example()
