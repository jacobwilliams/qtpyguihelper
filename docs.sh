#!/bin/bash
# Documentation build and serve script for vibegui

set -e

# Change to docs directory
cd "$(dirname "$0")/docs"

# Function to show usage
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build      Build the documentation (default)"
    echo "  clean      Clean the build directory"
    echo "  serve      Build and serve the documentation with live reload"
    echo "  open       Build and open the documentation in browser"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build    # Build the documentation"
    echo "  $0 serve    # Serve with live reload on http://127.0.0.1:8000"
    echo "  $0 open     # Build and open in default browser"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to build documentation
build_docs() {
    echo "Building documentation..."
    if command_exists make; then
        make html
    else
        sphinx-build -b html . _build/html
    fi
    echo "Documentation built successfully!"
    echo "Open file://$(pwd)/_build/html/index.html in your browser to view it."
}

# Function to clean build directory
clean_docs() {
    echo "Cleaning documentation build directory..."
    if command_exists make; then
        make clean
    else
        rm -rf _build
    fi
    echo "Build directory cleaned!"
}

# Function to serve documentation with live reload
serve_docs() {
    if ! command_exists sphinx-autobuild; then
        echo "sphinx-autobuild not found."
    fi

    echo "Starting documentation server with live reload..."
    echo "Documentation will be available at: http://127.0.0.1:8000"
    echo "Press Ctrl+C to stop the server."
    sphinx-autobuild . _build/html --host 127.0.0.1 --port 8000
}

# Function to build and open documentation
open_docs() {
    build_docs

    # Try to open in browser
    local html_file="file://$(pwd)/_build/html/index.html"

    if command_exists open; then
        # macOS
        open "$html_file"
    elif command_exists xdg-open; then
        # Linux
        xdg-open "$html_file"
    elif command_exists start; then
        # Windows
        start "$html_file"
    else
        echo "Could not automatically open browser."
        echo "Please open: $html_file"
    fi
}

# Main script logic
case "${1:-build}" in
    build)
        build_docs
        ;;
    clean)
        clean_docs
        ;;
    serve)
        serve_docs
        ;;
    open)
        open_docs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
