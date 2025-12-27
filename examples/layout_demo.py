"""
Demo showing different layout options across backends.
"""
import os
import sys
import subprocess

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import GuiBuilder, get_available_backends


def create_layout_demo(layout_type: str, backend: str = 'qt') -> None:
    """Create a demo with a specific layout type."""
    config = {
        "window": {
            "title": f"Layout Demo - {layout_type.title()} - {backend.upper()}",
            "width": 600,
            "height": 400
        },
        "layout": layout_type,
        "fields": [
            {"name": "name", "type": "text", "label": "Name", "placeholder": "Enter name"},
            {"name": "email", "type": "text", "label": "Email", "placeholder": "Enter email"},
            {"name": "age", "type": "number", "label": "Age", "min_value": 1, "max_value": 120},
            {"name": "subscribe", "type": "checkbox", "label": "Subscribe to newsletter"}
        ],
        "submit_button": True,
        "submit_label": "Submit",
        "cancel_button": True
    }

    # Use create_and_run() which properly handles QApplication for Qt backend
    GuiBuilder.create_and_run(config_dict=config, backend=backend)


def run_backend_test(backend: str, layout: str) -> subprocess.Popen:
    """Run a backend test in a subprocess."""
    cmd = [sys.executable, __file__, '--single', backend, layout]

    print(f"Starting {backend} backend with {layout} layout...")
    return subprocess.Popen(cmd)


if __name__ == "__main__":
    if '--single' in sys.argv:
        # Single backend mode (called from subprocess)
        backend = sys.argv[2] if len(sys.argv) > 2 else 'qt'
        layout = sys.argv[3] if len(sys.argv) > 3 else 'form'
        print(f"Running {backend} backend with {layout} layout...")
        create_layout_demo(layout, backend)
    else:
        # Multi-backend mode (spawn subprocesses)
        layout = sys.argv[1] if len(sys.argv) > 1 else 'form'

        print(f"Testing {layout} layout across all backends...")
        print("=" * 60)

        available_backends = get_available_backends()
        print(f"Available backends: {', '.join(available_backends)}")
        print("=" * 60)

        processes = []
        for backend in available_backends:
            proc = run_backend_test(backend, layout)
            processes.append((backend, proc))

        print(f"\nStarted {len(processes)} backend processes.")
        print("Close each window to continue, or Ctrl+C to exit all.\n")

        # Wait for all processes to complete
        try:
            for backend, proc in processes:
                proc.wait()
                print(f"{backend} backend finished.")
        except KeyboardInterrupt:
            print("\n\nTerminating all processes...")
            for backend, proc in processes:
                proc.terminate()
            print("Done.")