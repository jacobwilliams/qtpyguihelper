# Sphinx Documentation

This directory contains the Sphinx documentation for vibegui.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install vibegui[docs]
```

Or install Sphinx and the theme manually:

```bash
pip install sphinx sphinx-rtd-theme
```

### Building HTML Documentation

To build the HTML documentation:

```bash
cd docs
make html
```

The generated documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser to view it.

### Building Other Formats

Sphinx supports multiple output formats:

```bash
make html      # HTML documentation
make latex     # LaTeX documentation
make man       # Manual pages
make epub      # EPUB e-book format
make clean     # Clean build directory
```

### Live Reload During Development

For documentation development with auto-reload:

```bash
pip install sphinx-autobuild
sphinx-autobuild . _build/html
```

Then open http://127.0.0.1:8000 in your browser. The documentation will automatically rebuild when you save changes.

## Documentation Structure

- `conf.py` - Sphinx configuration file
- `index.rst` - Main documentation page
- `installation.rst` - Installation instructions
- `quickstart.rst` - Quick start guide
- `api/` - API documentation (auto-generated from docstrings)
- `examples.rst` - Usage examples
- `backends.rst` - Backend-specific documentation
- `_static/` - Static files (CSS, images, etc.)
- `_templates/` - Custom Sphinx templates

## Writing Documentation

### reStructuredText Primer

The documentation uses reStructuredText (RST) format. Here are some common patterns:

#### Headings
```rst
Main Title
==========

Section
-------

Subsection
~~~~~~~~~~

Subsubsection
^^^^^^^^^^^^^
```

#### Code Blocks
```rst
.. code-block:: python

   from vibegui import GuiBuilder
   gui = GuiBuilder.create_and_run(config_dict=config)
```

#### Links
```rst
:doc:`installation`           # Link to another document
:class:`TkGuiBuilder`        # Link to a class
:meth:`get_form_data`        # Link to a method
:ref:`section-label`         # Link to a section
```

#### API Documentation
```rst
.. automodule:: vibegui.utils
   :members:
   :undoc-members:
   :show-inheritance:
```

### Adding New Documentation

1. Create new `.rst` files in the appropriate location
2. Add them to the toctree in `index.rst` or relevant parent document
3. Use consistent heading styles and formatting
4. Include code examples where appropriate
5. Build and test the documentation before committing

### Best Practices

- Keep lines under 100 characters for readability
- Use consistent heading hierarchy
- Include practical examples in addition to API docs
- Write clear, concise descriptions
- Use proper cross-references instead of plain text
- Test all code examples to ensure they work
- Include screenshots for UI-related features (save in `_static/`)

## Deployment

The documentation can be deployed to various platforms:

- **Read the Docs**: Connect your repository for automatic builds
- **GitHub Pages**: Use GitHub Actions to build and deploy
- **Self-hosted**: Build HTML and serve with any web server

Example GitHub Actions workflow for automated deployment:

```yaml
name: Build Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        pip install -e .[docs]
    - name: Build documentation
      run: |
        cd docs
        make html
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```
