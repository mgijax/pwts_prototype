#!/bin/sh
source ../Configuration

echo "running all python tests"
python all_tests.py || exit 1;
