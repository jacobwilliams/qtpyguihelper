"""
Demo showing nested value support across backends.
"""
import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import GuiBuilder


def main() -> None:
    """Demonstrate nested value support."""
    # Form configuration with nested field names
    config = {
        "title": "User Profile",
        "fields": [
            {"name": "name", "type": "text", "label": "Full Name"},
            {"name": "address.street", "type": "text", "label": "Street Address"},
            {"name": "address.city", "type": "text", "label": "City"},
            {"name": "address.zip", "type": "text", "label": "ZIP Code"},
            {"name": "contact.email", "type": "text", "label": "Email"},
            {"name": "contact.phone", "type": "text", "label": "Phone"},
        ]
    }

    # Initial data with nested structure
    initial_data = {
        "name": "Jane Smith",
        "address": {
            "street": "456 Oak Avenue",
            "city": "Portland",
            "zip": "97201"
        },
        "contact": {
            "email": "jane.smith@example.com",
            "phone": "555-9876"
        }
    }

    def on_submit(data: dict) -> bool:
        """Handle form submission."""
        print("\n=== Submitted Data (Nested Structure) ===")
        print(f"Name: {data.get('name')}")
        print(f"Address: {data.get('address')}")
        print(f"Contact: {data.get('contact')}")
        print("\nFull data structure:")
        print(json.dumps(data, indent=2))
        return True  # Close dialog on submit

    # Create and run GUI with nested data
    gui = GuiBuilder(config_dict=config)
    gui.set_form_data(initial_data)
    gui.set_submit_callback(on_submit)
    gui.run()


if __name__ == "__main__":
    main()
