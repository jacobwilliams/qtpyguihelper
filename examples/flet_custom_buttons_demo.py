#!/usr/bin/env python3
"""
Flet custom buttons demo - demonstrates custom button callbacks in Flet backend.
Uses the same configuration as the Qt custom_buttons demo.
"""

import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main() -> None:
    """Run the Flet custom buttons demo."""
    # Force Flet backend
    from vibegui import set_backend
    set_backend('flet')
    print("✓ Flet backend selected")

    from vibegui import GuiBuilder
    import flet as ft

    print("Starting Flet Custom Buttons Demo...")

    # Load custom buttons configuration
    config_path = os.path.join(os.path.dirname(__file__), "custom_buttons.json")
    gui = GuiBuilder(config_path=config_path)

    def validate_data_callback(form_data: dict) -> None:
        """Validate form data."""
        issues = []

        if not form_data.get('first_name', '').strip():
            issues.append("First name is required")
        if not form_data.get('last_name', '').strip():
            issues.append("Last name is required")
        if not form_data.get('email', '').strip():
            issues.append("Email is required")
        elif '@' not in form_data.get('email', ''):
            issues.append("Email must contain @ symbol")

        # Convert age to int for comparison
        try:
            age = int(form_data.get('age', 0) or 0)
            if age < 18:
                issues.append("Age must be 18 or older")
        except (ValueError, TypeError):
            issues.append("Age must be a valid number")

        # Convert salary to float for comparison
        try:
            salary = float(form_data.get('salary', 0) or 0)
            if salary < 0:
                issues.append("Salary cannot be negative")
        except (ValueError, TypeError):
            issues.append("Salary must be a valid number")

        # Show validation results
        if issues:
            msg = "Validation Failed\n\nValidation Issues Found:\n\n• " + "\n• ".join(issues)
            gui._show_error(msg)
        else:
            gui._show_error("Validation Passed\n\nAll form data is valid!")

    def clear_all_callback(form_data: dict) -> None:
        """Clear all form fields."""
        # In Flet, we'll just clear directly without confirmation for simplicity
        # (Flet doesn't have built-in confirmation dialogs like Qt)
        gui.clear_form()
        print("Form cleared")
        gui._show_error("Form Cleared\n\nAll form fields have been cleared.")

    def preview_callback(form_data: dict) -> None:
        """Preview form data."""
        preview_text = "Form Data Preview:\n\n"

        for key, value in form_data.items():
            if key and value is not None:
                if isinstance(value, float):
                    preview_text += f"{key.replace('_', ' ').title()}: ${value:,.2f}\n"
                else:
                    preview_text += f"{key.replace('_', ' ').title()}: {value}\n"

        gui._show_error(preview_text)

    def export_json_callback(form_data: dict) -> None:
        """Export form data as JSON."""
        try:
            # For Flet, we'll export to a fixed location since file dialogs are more complex
            file_path = os.path.join(os.path.dirname(__file__), "exported_form_data.json")

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(form_data, f, indent=2, ensure_ascii=False)

            print(f"Form data exported to: {file_path}")
            gui._show_error(f"Export Successful\n\nForm data exported to:\n{file_path}")
        except Exception as e:
            gui._show_error(f"Export Failed\n\nFailed to export data:\n{str(e)}")

    def on_submit_custom_buttons(form_data: dict) -> None:
        """Handle form submission."""
        print("Form submitted with data:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        gui._show_error("Form Submitted\n\nForm data has been submitted successfully!")

    def on_cancel_custom_buttons() -> None:
        """Handle form cancellation."""
        print("Form cancelled")
        gui._show_error("Cancelled\n\nForm submission was cancelled.")

    # Register custom button callbacks
    gui.set_custom_button_callback("validate", validate_data_callback)
    gui.set_custom_button_callback("clear", clear_all_callback)
    gui.set_custom_button_callback("preview", preview_callback)
    gui.set_custom_button_callback("export", export_json_callback)

    # Register standard callbacks
    gui.set_submit_callback(on_submit_custom_buttons)
    gui.set_cancel_callback(on_cancel_custom_buttons)

    print("Custom buttons available:")
    for button_name in gui.get_custom_button_names():
        print(f"  - {button_name}")

    # Show the GUI
    gui.show()


if __name__ == "__main__":
    main()
