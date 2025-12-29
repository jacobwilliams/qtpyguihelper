"""Field change callbacks example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {"title": "Dynamic Form", "width": 400, "height": 300},
    "fields": [
        {"name": "user_type", "label": "User Type", "type": "select",
         "options": ["Student", "Teacher", "Administrator"], "required": True},
        {"name": "student_id", "label": "Student ID", "type": "text"},
        {"name": "grade_level", "label": "Grade Level", "type": "number", "min_value": 1, "max_value": 12},
        {"name": "department", "label": "Department", "type": "text"},
        {"name": "admin_level", "label": "Admin Level", "type": "select",
         "options": ["Level 1", "Level 2", "Level 3"]}
    ]
}

def on_user_type_change(field_name, value):
    print(f"User type changed to: {value}")

    # Enable/disable fields based on user type
    if value == "Student":
        gui.set_field_value("student_id", "")
        gui.set_field_value("grade_level", "")
        # In a real implementation, you would show/hide fields here
        print("Showing student-specific fields")
    elif value == "Teacher":
        gui.set_field_value("department", "")
        print("Showing teacher-specific fields")
    elif value == "Administrator":
        gui.set_field_value("admin_level", "")
        print("Showing administrator-specific fields")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.add_field_change_callback('user_type', on_user_type_change)
    gui.show()

    sys.exit(app.exec())
