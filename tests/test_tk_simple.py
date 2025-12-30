"""
Simple tkinter test to check if basic window creation works on macOS.
"""

import sys
import traceback
import pytest

@pytest.mark.gui
@pytest.mark.tk
def test_basic_tkinter() -> None:
    """Test basic tkinter window creation."""
    print("Testing basic tkinter functionality...")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")

    try:
        import tkinter as tk
        print("✓ tkinter import successful")

        # Test basic Tk creation
        print("Creating Tk root window...")
        root = tk.Tk()
        print("✓ Tk root window created")

        # Set some basic properties
        root.title("Test Window")
        root.geometry("300x200")
        print("✓ Window properties set")

        # Create a simple widget
        label = tk.Label(root, text="Hello, tkinter!")
        label.pack()
        print("✓ Label widget created and packed")

        # Get tkinter version info
        print(f"✓ tkinter version: {tk.TkVersion}")
        print(f"✓ Tcl version: {tk.TclVersion}")

        # Don't show the window, just test creation
        print("Destroying window...")
        root.destroy()
        print("✓ Window destroyed successfully")

        assert True, "tkinter basic test passed"

    except Exception as e:
        print(f"✗ Error: {e}")
        print(f"✗ Error type: {type(e).__name__}")
        print("✗ Full traceback:")
        traceback.print_exc()
        assert False, "tkinter basic test failed"

@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_with_widgets() -> None:
    """Test tkinter with various widget types."""
    print("\nTesting tkinter with various widgets...")

    try:
        import tkinter as tk
        from tkinter import ttk

        root = tk.Tk()
        root.title("Widget Test")
        root.geometry("400x300")

        # Create various widget types
        widgets = []

        # Entry widget
        entry = tk.Entry(root)
        entry.insert(0, "test text")
        entry.pack()
        widgets.append(("entry", entry))

        # Text widget
        text = tk.Text(root, height=3)
        text.insert("1.0", "test text area")
        text.pack()
        widgets.append(("text", text))

        # Checkbox
        var1 = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text="Test Checkbox", variable=var1)
        checkbox.pack()
        widgets.append(("checkbox", checkbox))

        # Combobox
        combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
        combo.set("Option 1")
        combo.pack()
        widgets.append(("combobox", combo))

        print(f"✓ Created {len(widgets)} widgets successfully")

        # Test getting values
        values = {}
        values['entry'] = entry.get()
        values['text'] = text.get("1.0", tk.END).strip()
        values['checkbox'] = var1.get()
        values['combo'] = combo.get()

        print(f"✓ Widget values: {values}")

        root.destroy()
        print("✓ Widgets test completed successfully")

        assert True, "tkinter widget test passed"

    except Exception as e:
        print(f"✗ Widget test error: {e}")
        traceback.print_exc()
        assert False, "tkinter widget test failed"
