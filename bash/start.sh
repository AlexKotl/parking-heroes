#!/bin/bash
echo "Starting Python in env. "
cd ..
nohup pipenv run python parking.py &
#sleep 5
#nohup python -u parking.py &> ./../parking.log &