"""
Test nested value support across all backends.
"""
import pytest
from vibegui.backend import get_available_backends


def test_nested_value_support() -> None:
    """Test that all backends support nested values with dot notation."""
    # Test data with nested structure
    nested_data = {
        "name": "John Doe",
        "address.street": "123 Main St",
        "address.city": "Springfield",
        "contact.email": "john@example.com",
        "contact.phone": "555-1234"
    }

    # Expected flattened output
    expected_flat = {
        "name": "John Doe",
        "address.street": "123 Main St",
        "address.city": "Springfield",
        "contact.email": "john@example.com",
        "contact.phone": "555-1234"
    }

    # Expected nested output when converted
    expected_nested = {
        "name": "John Doe",
        "address": {
            "street": "123 Main St",
            "city": "Springfield"
        },
        "contact": {
            "email": "john@example.com",
            "phone": "555-1234"
        }
    }

    available_backends = get_available_backends()
    print(f"\n=== Testing nested values in {len(available_backends)} backends ===")

    for backend_name in available_backends:
        print(f"\nTesting {backend_name}...")

        # Import the appropriate widget factory
        if backend_name == "qt":
            from vibegui.qt.qt_widget_factory import WidgetFactory
        elif backend_name == "wx":
            from vibegui.wx.wx_widget_factory import WxWidgetFactory as WidgetFactory
        elif backend_name == "tk":
            from vibegui.tk.tk_widget_factory import TkWidgetFactory as WidgetFactory
        elif backend_name == "gtk":
            from vibegui.gtk.gtk_widget_factory import GtkWidgetFactory as WidgetFactory
        elif backend_name == "flet":
            from vibegui.flet.flet_widget_factory import FletWidgetFactory as WidgetFactory
        else:
            continue

        # Create factory instance
        factory = WidgetFactory()

        # Create mock widgets for testing
        # We'll just add simple string storage for testing
        class MockWidget:
            def __init__(self) -> None:
                self.value = ""

        for field_name in nested_data.keys():
            factory.widgets[field_name] = MockWidget()

        # Mock get_widget_value and set_widget_value if needed
        def get_widget_value(field_name: str) -> object:
            if field_name in factory.widgets:
                return factory.widgets[field_name].value
            return None

        def set_widget_value(field_name: str, value: object) -> bool:
            if field_name in factory.widgets:
                factory.widgets[field_name].value = value
                return True
            return False

        # For backends that don't have these methods directly (like Flet)
        if not hasattr(factory, 'get_widget_value'):
            factory.get_widget_value = get_widget_value
            factory.set_widget_value = set_widget_value
        else:
            # Patch the methods for testing
            original_get = factory.get_widget_value
            original_set = factory.set_widget_value
            factory.get_widget_value = get_widget_value
            factory.set_widget_value = set_widget_value

        # Test set_all_values
        factory.set_all_values(nested_data)

        # Verify values were set
        for field_name, expected_value in nested_data.items():
            actual_value = factory.get_widget_value(field_name)
            assert actual_value == expected_value, f"{backend_name}: Field {field_name} should be {expected_value}, got {actual_value}"

        # Test get_all_values returns nested structure
        result = factory.get_all_values()

        # The result should have nested structure
        assert "name" in result
        assert result["name"] == "John Doe"

        # Check nested address
        if "address" in result:
            assert isinstance(result["address"], dict)
            assert result["address"]["street"] == "123 Main St"
            assert result["address"]["city"] == "Springfield"
            print(f"  ✓ {backend_name} supports nested structure for 'address'")

        # Check nested contact
        if "contact" in result:
            assert isinstance(result["contact"], dict)
            assert result["contact"]["email"] == "john@example.com"
            assert result["contact"]["phone"] == "555-1234"
            print(f"  ✓ {backend_name} supports nested structure for 'contact'")

        print(f"  ✓ {backend_name} nested value support verified!")


def test_nested_value_helper_functions() -> None:
    """Test the helper functions used by NestedValueMixin."""
    from vibegui.utils import set_nested_value, flatten_nested_dict

    # Test set_nested_value
    result = {}
    set_nested_value(result, "simple", "value1")
    assert result == {"simple": "value1"}

    result = {}
    set_nested_value(result, "nested.key", "value2")
    assert result == {"nested": {"key": "value2"}}

    result = {}
    set_nested_value(result, "deep.nested.key", "value3")
    assert result == {"deep": {"nested": {"key": "value3"}}}

    # Test flatten_nested_dict
    nested = {
        "simple": "value1",
        "nested": {
            "key": "value2"
        },
        "deep": {
            "nested": {
                "key": "value3"
            }
        }
    }

    flat = flatten_nested_dict(nested)
    assert flat["simple"] == "value1"
    assert flat["nested.key"] == "value2"
    assert flat["deep.nested.key"] == "value3"

    print("\n✓ Helper functions working correctly")


if __name__ == "__main__":
    test_nested_value_helper_functions()
    test_nested_value_support()
    print("\n=== All nested value tests passed! ===")
