#!/usr/bin/env python3
"""
Complete example demonstrating data persistence with QtPyGuiHelper.

This example shows how to:
1. Create a GUI from a JSON configuration
2. Load existing data from a JSON file
3. Allow users to edit the data
4. Save the updated data back to JSON files
"""

import sys
import os
import json

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from qtpyguihelper import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox, QFileDialog

    def create_config_editor():
        """Create a configuration editor with data persistence."""

        # Define the GUI configuration
        config = {
            "window": {
                "title": "Application Configuration Editor",
                "width": 600,
                "height": 500,
                "resizable": True
            },
            "layout": "form",
            "fields": [
                {
                    "name": "app_name",
                    "type": "text",
                    "label": "Application Name",
                    "required": True,
                    "default_value": "My Application",
                    "placeholder": "Enter application name"
                },
                {
                    "name": "version",
                    "type": "text",
                    "label": "Version",
                    "default_value": "1.0.0",
                    "placeholder": "e.g., 1.2.3"
                },
                {
                    "name": "debug_mode",
                    "type": "checkbox",
                    "label": "Enable debug mode",
                    "default_value": False
                },
                {
                    "name": "log_level",
                    "type": "select",
                    "label": "Log Level",
                    "options": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    "default_value": "INFO"
                },
                {
                    "name": "max_connections",
                    "type": "number",
                    "label": "Max Connections",
                    "min_value": 1,
                    "max_value": 1000,
                    "default_value": 100
                },
                {
                    "name": "timeout",
                    "type": "number",
                    "label": "Timeout (seconds)",
                    "min_value": 1,
                    "max_value": 300,
                    "default_value": 30
                },
                {
                    "name": "database_url",
                    "type": "text",
                    "label": "Database URL",
                    "placeholder": "postgres://user:pass@host:port/db"
                },
                {
                    "name": "api_key",
                    "type": "password",
                    "label": "API Key",
                    "placeholder": "Enter your API key"
                },
                {
                    "name": "backup_enabled",
                    "type": "checkbox",
                    "label": "Enable automatic backups",
                    "default_value": True
                },
                {
                    "name": "backup_interval",
                    "type": "range",
                    "label": "Backup Interval (hours)",
                    "min_value": 1,
                    "max_value": 24,
                    "default_value": 6
                },
                {
                    "name": "theme",
                    "type": "select",
                    "label": "UI Theme",
                    "options": ["Light", "Dark", "Auto"],
                    "default_value": "Auto"
                },
                {
                    "name": "notifications",
                    "type": "checkbox",
                    "label": "Enable notifications",
                    "default_value": True
                }
            ],
            "submit_button": True,
            "submit_label": "Save Configuration",
            "cancel_button": True,
            "cancel_label": "Cancel"
        }

        return config

    def main():
        """Main function to run the configuration editor."""

        # Create application
        app = QApplication(sys.argv)

        # Create GUI from configuration
        config = create_config_editor()
        gui = GuiBuilder(config_dict=config)

        # Try to load existing configuration
        config_file = "app_config.json"
        if os.path.exists(config_file):
            success = gui.load_data_from_file(config_file)
            if success:
                print(f"Loaded existing configuration from {config_file}")

                # Show a message to the user
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Configuration Loaded")
                msg.setText(f"Existing configuration loaded from {config_file}")
                msg.exec()
        else:
            print("No existing configuration found, using defaults")

        # Set up save functionality
        def on_save_config(form_data):
            """Handle configuration save."""
            print("Configuration data:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

            # Ask user where to save
            file_path, _ = QFileDialog.getSaveFileName(
                gui,
                "Save Configuration",
                config_file,
                "JSON files (*.json);;All files (*.*)"
            )

            if file_path:
                # Save the configuration
                success = gui.save_data_to_file(file_path)
                if success:
                    print(f"Configuration saved to {file_path}")

                    # Also save with metadata for reference
                    metadata_file = file_path.replace('.json', '_with_metadata.json')
                    gui.save_data_with_metadata_to_file(metadata_file)

                    # Show success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Configuration Saved")
                    msg.setText(f"Configuration saved successfully!\n\nFiles created:\n• {file_path}\n• {metadata_file}")
                    msg.exec()
                else:
                    # Show error message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Save Error")
                    msg.setText("Failed to save configuration file.")
                    msg.exec()

        def on_cancel():
            """Handle cancel action."""
            # Ask if user wants to exit without saving
            reply = QMessageBox.question(
                gui,
                "Exit without saving?",
                "Are you sure you want to exit without saving changes?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                app.quit()

        # Connect callbacks
        gui.set_submit_callback(on_save_config)
        gui.set_cancel_callback(on_cancel)

        # Connect to field changes for real-time feedback
        def on_field_change(field_name, value):
            """Handle field changes."""
            print(f"Field '{field_name}' changed to: {value}")

            # Example: Update window title to show unsaved changes
            if "*" not in gui.windowTitle():
                gui.setWindowTitle(gui.windowTitle() + " *")

        gui.fieldChanged.connect(on_field_change)

        # Show the GUI
        gui.show()

        print("Configuration editor started. You can:")
        print("1. Edit the configuration values")
        print("2. Click 'Save Configuration' to save to a file")
        print("3. The app will load existing config on next startup")

        # Run the application
        app.exec()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have a Qt binding installed (PySide6 or PyQt6) and qtpy is available.")
    sys.exit(1)
