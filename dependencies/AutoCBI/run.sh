#!/bin/bash

# Input file
input_file="gccbugs_input.txt"
output_file="gccbugs"

# Check if the input file exists
if [[ ! -f $input_file ]]; then
    echo "Input file '$input_file' not found!"
    exit 1
fi

# Process each line of the input file
while IFS= read -r line; do
    # Write the line to the output file
    echo "$line" > "$output_file"
    
    # Run the Python script with the output file as an argument
    python3.9 gcc-run.py "$output_file"
done < "$input_file"