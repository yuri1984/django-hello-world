#!/bin/bash
#
# Run custom admin command and parse output
#
echo "Counting models..."

# NOTE: Change this to your virtual environment path in order to run script properly
source ../../venv/bin/activate

# Filename with date
_now=$(date +"%m_%d_%Y")
_file="./$_now.dat"
python manage.py modelcount 2> "$_file"

