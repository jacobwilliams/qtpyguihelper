"""Tabbed interface example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {
        "title": "Employee Management",
        "width": 600,
        "height": 500
    },
    "fields": [
        # Personal Information fields
        {"name": "first_name", "label": "First Name", "type": "text", "required": True},
        {"name": "last_name", "label": "Last Name", "type": "text", "required": True},
        {"name": "employee_id", "label": "Employee ID", "type": "text", "required": True},
        {"name": "department", "label": "Department", "type": "select",
         "options": ["Engineering", "Sales", "Marketing", "HR", "Finance"]},
        {"name": "hire_date", "label": "Hire Date", "type": "date", "required": True},
        # Contact Details fields
        {"name": "email", "label": "Work Email", "type": "email", "required": True},
        {"name": "phone", "label": "Phone Number", "type": "text"},
        {"name": "emergency_contact", "label": "Emergency Contact", "type": "text"},
        {"name": "address", "label": "Address", "type": "textarea"},
        # Job Details fields
        {"name": "position", "label": "Position", "type": "text", "required": True},
        {"name": "salary", "label": "Salary", "type": "number", "min_value": 0},
        {"name": "full_time", "label": "Full-time Employee", "type": "checkbox", "default_value": True},
        {"name": "start_time", "label": "Start Time", "type": "time"},
        {"name": "benefits", "label": "Benefits Package", "type": "select",
         "options": ["Basic", "Standard", "Premium"]}
    ],
    "use_tabs": True,
    "tabs": [
        {
            "name": "personal_info",
            "title": "Personal Information",
            "fields": ["first_name", "last_name", "employee_id", "department", "hire_date"]
        },
        {
            "name": "contact_details",
            "title": "Contact Details",
            "fields": ["email", "phone", "emergency_contact", "address"]
        },
        {
            "name": "job_details",
            "title": "Job Details",
            "fields": ["position", "salary", "full_time", "start_time", "benefits"]
        }
    ],
    "submit_button": True,
    "submit_label": "Save Employee",
    "cancel_button": True
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.show()

    sys.exit(app.exec())
