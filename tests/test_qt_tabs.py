#!/usr/bin/env python3
"""
Test script for Qt backend tabs to verify field expansion.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_qt_tabs() -> None:
    """Test Qt backend with tabs to verify field expansion."""
    print("Testing Qt Backend with Tabs...")

    try:
        # Force Qt backend
        from vibegui import set_backend
        set_backend('qt')
        print("✓ Qt backend selected")

        # Import Qt
        from qtpy.QtWidgets import QApplication, QMessageBox

        # Use the existing tabbed configuration file
        config_path = os.path.join(os.path.dirname(__file__), "..", "examples", "tabbed_config.json")
        if not os.path.exists(config_path):
            print(f"✗ Configuration file not found: {config_path}")
            assert False, "Configuration file not found"

        # Create Qt application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Create GUI builder with Qt backend using the config file
        from vibegui import GuiBuilder
        gui_builder = GuiBuilder(config_path=config_path)

        # Set up callbacks
        def on_submit(form_data: dict) -> None:
            try:
                print("Qt tabs form submitted:")
                print("="*50)
                for key, value in form_data.items():
                    print(f"  {key}: {value}")
                print("="*50)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Configuration saved successfully!\n\nCheck the console for submitted data.")
                msg.exec()
            except Exception as e:
                print(f"Error in submit callback: {e}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText(f"Error saving configuration: {e}")
                msg.exec()

        def on_cancel() -> None:
            print("Qt tabs form cancelled")
            # Close the dialog
            gui_builder.close()

        def load_defaults(_form_data: dict) -> None:
            """Load default configuration values."""
            defaults = {
                "app_name": "My Demo Application",
                "version": "2.0.0",
                "author": "Demo User",
                "description": "This is a demo application for testing field expansion in tabs.",
                "debug_mode": True,
                "log_level": "DEBUG",
                "max_connections": 200,
                "timeout": 60,
                "database_url": "postgres://demo:password@localhost:5432/demo_db",
                "api_key": "demo_api_key_12345",
                "theme": "Dark",
                "accent_color": "#FF5722",
                "font_size": 16,
                "backup_enabled": True,
                "backup_location": "/home/user/backups",
                "backup_interval": 12,
                "email_notifications": True,
                "notification_email": "demo@example.com"
            }
            gui_builder.set_form_data(defaults)
            print("Default values loaded")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Defaults Loaded")
            msg.setText("Default configuration values loaded successfully!")
            msg.exec()

        def clear_all(_form_data: dict) -> None:
            """Clear all form fields."""
            reply = QMessageBox.question(
                None,
                "Confirm Clear",
                "Are you sure you want to clear all fields?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                gui_builder.clear_form()
                print("All fields cleared")

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Cleared")
                msg.setText("All form fields have been cleared.")
                msg.exec()

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)

        # Only register custom button callbacks if the buttons exist
        custom_button_names = gui_builder.get_custom_button_names()
        if "load_defaults" in custom_button_names:
            gui_builder.set_custom_button_callback("load_defaults", load_defaults)
        if "clear_all" in custom_button_names:
            gui_builder.set_custom_button_callback("clear_all", clear_all)

        # Show the GUI
        gui_builder.show()

        print("✓ Qt tabbed GUI created and shown")
        print("  - Custom buttons available:", custom_button_names)
        print("\nInstructions:")
        print("  1. Resize the window to test field expansion")
        print("  2. Switch between tabs to verify all fields expand properly")
        if custom_button_names:
            print("  3. Try the custom buttons if available")
        print("  4. Submit to see the form data structure")
        print("  5. Compare field expansion behavior with wxPython version")

        # Run the application
        app.exec()

    except ImportError as e:
        print(f"✗ Qt not available: {e}")
    except Exception as e:
        print(f"✗ Error with Qt tabs test: {e}")
        import traceback
        traceback.print_exc()

