#!/bin/bash

# Get the path of the python executable
python_path=$(which python)

# Check if python is installed
if [[ -z $python_path ]]; then
    # If python is not installed point to python3 executable
    python_path=$(which python3)
fi

# If both are not installed throw error
if [[ -z $python_path ]]; then
    echo "Error: Python or Python3 not found!"
    exit 1
fi

"$python_path" basic_3.py $1 $2
