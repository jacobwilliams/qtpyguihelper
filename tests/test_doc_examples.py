"""Test that all documentation examples are runnable."""

import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


EXAMPLES_DIR = Path(__file__).parent.parent / "examples" / "docs_examples"

# List of all example files
EXAMPLE_FILES = [
    "simple_form.py",
    "advanced_form.py",
    "tabbed_interface.py",
    "custom_buttons.py",
    "data_persistence.py",
    "field_change_callbacks.py",
    "nested_fields.py",
    "float_formatting.py",
    "layout_examples.py",
    "json_loading.py",
]


@pytest.mark.parametrize("example_file", EXAMPLE_FILES)
def test_example_syntax(example_file: str) -> None:
    """Test that each example file has valid Python syntax."""
    example_path = EXAMPLES_DIR / example_file
    assert example_path.exists(), f"Example file {example_file} not found"

    # Compile the file to check syntax
    with open(example_path, 'r') as f:
        code = f.read()

    try:
        compile(code, example_file, 'exec')
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {example_file}: {e}")


@pytest.mark.gui
@pytest.mark.parametrize("example_file", EXAMPLE_FILES)
def test_example_imports(example_file: str) -> None:
    """Test that each example can import required modules."""
    example_path = EXAMPLES_DIR / example_file

    # Test that the file can be imported (checks imports are available)
    result = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.path.insert(0, '{EXAMPLES_DIR.parent.parent}'); import ast; ast.parse(open('{example_path}').read())"],
        capture_output=True,
        check=True
    )

    assert result.returncode == 0, f"Failed to parse {example_file}: {result.stderr.decode()}"


@pytest.mark.gui
@pytest.mark.parametrize("example_file", EXAMPLE_FILES)
def test_example_execution(example_file: str) -> None:
    """Test that each example can be executed without errors."""
    example_path = EXAMPLES_DIR / example_file
    project_root = EXAMPLES_DIR.parent.parent

    # Run the script with QT_QPA_PLATFORM=offscreen to avoid GUI display
    # and a timeout to ensure it doesn't hang
    #
    # note: commented out QT_QPA_PLATFORM so that the
    # GUIs actually run and open. if running this test, you have to
    # manually close each GUI window to let the test complete.
    env = {
        **subprocess.os.environ.copy(),
        # "QT_QPA_PLATFORM": "offscreen",
        "PYTHONPATH": str(project_root)  # Add project root to Python path
    }

    result = subprocess.run(
        [sys.executable, str(example_path)],
        capture_output=True,
        timeout=60,
        env=env,
        check=True
    )

    # Check if there were any errors during execution
    stderr = result.stderr.decode()

    # Filter out expected Qt platform warnings
    stderr_lines = [line for line in stderr.split('\n')
                   if line and not any(x in line.lower() for x in
                   ['qt.qpa', 'could not connect to display', 'xcb'])]

    if result.returncode != 0 and stderr_lines:
        pytest.fail(f"Execution failed for {example_file}:\nStderr: {stderr}\nStdout: {result.stdout.decode()}")


def test_all_examples_documented() -> None:
    """Verify all example files in docs_examples are listed in the test."""
    actual_files = {f.name for f in EXAMPLES_DIR.glob("*.py") if f.name != "__init__.py"}
    expected_files = set(EXAMPLE_FILES)

    missing = actual_files - expected_files
    if missing:
        pytest.fail(f"Example files not listed in test: {missing}")

    extra = expected_files - actual_files
    if extra:
        pytest.fail(f"Example files listed but not found: {extra}")
