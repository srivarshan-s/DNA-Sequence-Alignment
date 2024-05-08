#!/bin/bash

# Get the path of the python3 executable
python_path=$(which python3)

# Check if python3 is installed
if [[ -z "$python_path" ]]; then
    # If python is not installed point to python executable
    python_path=$(which python)
fi

# If both are not installed throw error
if [[ -z "$python_path" ]]; then
    echo "Error: Python or Python3 not found!"
    exit 1
fi

"$python_path" efficient_3.py $1 $2
