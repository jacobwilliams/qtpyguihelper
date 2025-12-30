#!/usr/bin/env python3
"""Test tkinter GUI with run() method."""

import pytest
from vibegui import set_backend, GuiBuilder

@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_gui() -> None:
    # Set tkinter backend
    set_backend('tk')

    # Create config
    config = {
        'window': {'title': 'Tkinter Test GUI', 'width': 500, 'height': 400},
        'fields': [
            {'name': 'name', 'type': 'text', 'label': 'Your Name', 'default_value': 'John Doe'},
            {'name': 'age', 'type': 'int', 'label': 'Age', 'default_value': 25},
            {'name': 'email', 'type': 'email', 'label': 'Email', 'default_value': 'john@example.com'},
            {'name': 'subscribe', 'type': 'checkbox', 'label': 'Subscribe to newsletter', 'default_value': True}
        ]
    }

    # Create and run GUI
    gui = GuiBuilder(config_dict=config)
    print("Starting tkinter GUI...")
    gui.run()  # This should show the window and start the event loop

    assert True, "Tkinter GUI should run without errors"