#!/bin/bash

# Get the path of the python executable
python_path=$(which python)

# Check if python is installed
if [[ -z "$python_path" ]]; then
    # If python is not installed point to python3 executable
    python_path=$(which python3)
fi

# If both are not installed throw error
if [[ -z "$python_path" ]]; then
    echo "Error: Python or Python3 not found!"
    exit 1
fi

# Check if a directory path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Get the directory from command line argument
directory=$1

# Check if the provided directory exists
if [ ! -d "$directory" ]; then
    echo "Error: Directory does not exist!"
    exit 1
fi

# Initialize an empty array to hold the output files
files=()

# Use a while loop to read filenames into the array
while IFS= read -r -d $'\0' file; do
    files+=("$file")
done < <(find "$directory" -maxdepth 1 -type f -print0)

# Check if files were found
if [ ${#files[@]} -eq 0 ]; then
    echo "No files found in the directory."
    exit 1
fi

# Loop over each file and pass it to the test script
for file in "${files[@]}"; do
    "$python_path" test.py "$file"
done

