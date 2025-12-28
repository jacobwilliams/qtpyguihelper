#!/usr/bin/env python3
"""Test tooltip functionality across all backends."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vibegui


def main() -> None:
    """Run tooltip test with specified backend."""
    backend = sys.argv[1] if len(sys.argv) > 1 else 'qt'

    print(f"Testing tooltips with {backend} backend...")
    print("Hover over fields to see tooltips!")

    vibegui.GuiBuilder.create_and_run(
        config_path='examples/tooltip_test.json',
        backend=backend
    )


if __name__ == '__main__':
    main()
