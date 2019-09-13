#!/bin/bash
echo "Stopping Python script"
ps -ef | grep "parking.py" | grep -v grep | awk '{print $2}' | xargs kill