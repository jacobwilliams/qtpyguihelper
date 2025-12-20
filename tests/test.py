from qtpyguihelper import GuiBuilder

config = {
    "window": {"title": "My App", "width": 400, "height": 300},
    "fields": [
        {"name": "username", "label": "Username", "type": "text", "required": True},
        {"name": "email", "label": "Email", "type": "email", "required": True},
        {"name": "age", "label": "Age", "type": "number"}
    ]
}

# Create and run the GUI
gui = GuiBuilder.create_and_run(config_dict=config, backend='qt')
