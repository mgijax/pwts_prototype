#!/bin/bash
cd ..
source Configuration

APP_CONFIG_FILE=$PWTS/config/test.config.py
export APP_CONFIG_FILE

cd tests

echo 'Running acceptance tests'

python all_tests.py
if [ $? -ne 0 ]; then
        exit 1
fi
