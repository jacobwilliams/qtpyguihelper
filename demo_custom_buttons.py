#!/usr/bin/env python3
"""
Demo script showing how to use custom buttons with callbacks in qtpyguihelper.
"""

import sys
import json
from pathlib import Path
from qtpy.QtWidgets import QApplication, QMessageBox, QFileDialog

# Add the qtpyguihelper module to the path
sys.path.insert(0, str(Path(__file__).parent))

from qtpyguihelper import GuiBuilder


def validate_data_callback(form_data):
    """Callback for the Validate Data button."""
    # Perform some validation
    issues = []

    if not form_data.get('first_name', '').strip():
        issues.append("First name is required")
    if not form_data.get('last_name', '').strip():
        issues.append("Last name is required")
    if not form_data.get('email', '').strip():
        issues.append("Email is required")
    elif '@' not in form_data.get('email', ''):
        issues.append("Email must contain @ symbol")

    age = form_data.get('age', 0)
    if age < 18:
        issues.append("Age must be 18 or older")

    salary = form_data.get('salary', 0)
    if salary < 0:
        issues.append("Salary cannot be negative")

    # Show validation results
    if issues:
        msg = "Validation Issues Found:\n\n• " + "\n• ".join(issues)
        QMessageBox.warning(None, "Validation Failed", msg)
    else:
        QMessageBox.information(None, "Validation Passed", "All form data is valid!")


def clear_all_callback(form_data):
    """Callback for the Clear All button."""
    # Note: form_data parameter is included for consistency with other callbacks
    # Ask for confirmation
    reply = QMessageBox.question(
        None,
        "Confirm Clear",
        "Are you sure you want to clear all form data?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        # Access the global GUI builder reference to clear the form
        global gui_builder_instance
        if 'gui_builder_instance' in globals() and gui_builder_instance:
            gui_builder_instance.clear_form()
            QMessageBox.information(None, "Form Cleared", "All form fields have been cleared.")
        else:
            QMessageBox.information(None, "Clear Requested", "Form would be cleared (no GUI reference available)")


# Global reference to the GUI builder for callbacks that need to access it
gui_builder_instance = None


def preview_callback(form_data):
    """Callback for the Preview button."""
    # Create a formatted preview of the data
    preview_text = "Form Data Preview:\n\n"

    for key, value in form_data.items():
        if key and value is not None:
            if isinstance(value, float):
                preview_text += f"{key.replace('_', ' ').title()}: ${value:,.2f}\n"
            else:
                preview_text += f"{key.replace('_', ' ').title()}: {value}\n"

    QMessageBox.information(None, "Form Data Preview", preview_text)


def export_json_callback(form_data):
    """Callback for the Export JSON button."""
    # Open file dialog to save JSON
    file_path, _ = QFileDialog.getSaveFileName(
        None,
        "Export Form Data",
        "form_data.json",
        "JSON Files (*.json);;All Files (*)"
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(form_data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(None, "Export Successful", f"Form data exported to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Export Failed", f"Failed to export data:\n{str(e)}")


def on_submit(form_data):
    """Callback for the main Submit button."""
    print("Form submitted with data:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")

    QMessageBox.information(None, "Form Submitted", "Form data has been submitted successfully!")


def on_cancel():
    """Callback for the Cancel button."""
    print("Form cancelled")
    QMessageBox.information(None, "Cancelled", "Form submission was cancelled.")


def main():
    """Main function to run the custom buttons demo."""
    global gui_builder_instance

    app = QApplication(sys.argv)

    # Load the custom buttons configuration
    config_path = Path(__file__).parent / "examples" / "custom_buttons.json"

    if not config_path.exists():
        print(f"Configuration file not found: {config_path}")
        return 1

    try:
        # Create the GUI builder (this automatically builds the GUI)
        gui_builder_instance = GuiBuilder(str(config_path))

        # Register callbacks for custom buttons
        gui_builder_instance.set_custom_button_callback("validate", validate_data_callback)
        gui_builder_instance.set_custom_button_callback("clear", clear_all_callback)
        gui_builder_instance.set_custom_button_callback("preview", preview_callback)
        gui_builder_instance.set_custom_button_callback("export", export_json_callback)

        # Register standard callbacks
        gui_builder_instance.set_submit_callback(on_submit)
        gui_builder_instance.set_cancel_callback(on_cancel)

        # Show the GUI
        gui_builder_instance.show()

        print("Custom Buttons Demo started!")
        print("Available custom buttons:")
        for button_name in gui_builder_instance.get_custom_button_names():
            print(f"  - {button_name}")

        return app.exec()

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
