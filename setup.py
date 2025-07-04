"""
Setup script for QtPyGuiHelper library.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "A Python library for creating PySide6 GUIs from JSON configuration files."

# Read requirements
def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return ['PySide6>=6.5.0']

setup(
    name="qtpyguihelper",
    version="1.0.0",
    author="QtPyGuiHelper Team",
    author_email="",
    description="A Python library for creating PySide6 GUIs from JSON configuration files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qtpyguihelper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "qtpyguihelper-demo=demo:main",
        ],
    },
    include_package_data=True,
    package_data={
        "qtpyguihelper": ["*.py"],
        "": ["examples/*.json", "README.md", "requirements.txt"],
    },
    keywords="pyside6 qt gui json configuration form builder",
    project_urls={
        "Documentation": "https://github.com/yourusername/qtpyguihelper/blob/main/README.md",
        "Source": "https://github.com/yourusername/qtpyguihelper",
        "Tracker": "https://github.com/yourusername/qtpyguihelper/issues",
    },
)
