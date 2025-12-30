#!/bin/bash

#
# Run all the tests.
#

# Exit immediately if any command fails
set -e
# Optionally show commands as they execute
# set -x

# Loop over all test_*.py files in the tests directory
# Run each test file independently to avoid interference
for test_file in tests/test_*.py; do
    python -m pytest "$test_file" -v
done