#!/bin/bash
echo "Starting Python in env. "
touch started.log
cd ..
nohup pipenv run python -u parking.py &