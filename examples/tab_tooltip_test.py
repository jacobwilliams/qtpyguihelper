#!/usr/bin/env python3
"""Test tab tooltip functionality across all backends."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vibegui


def main():
    """Run tab tooltip test with specified backend."""
    backend = sys.argv[1] if len(sys.argv) > 1 else 'qt'

    print(f"Testing tab tooltips with {backend} backend...")
    print("Hover over the tab headers to see tooltips!")

    vibegui.GuiBuilder.create_and_run(
        config_path='examples/tab_tooltip_test.json',
        backend=backend
    )


if __name__ == '__main__':
    main()
