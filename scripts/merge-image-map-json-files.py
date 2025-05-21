# ./scripts/merge-image-map-json-files.sh \
#    /path/to/json-file1.json \
#    /path/to/json-file2.json
#    /path/to/output/output_file.json
#
# After running this script, you will see output in /path/to/output/output_file.json
#

import os
import sys
import json

def check_arguments():
    if len(sys.argv) != 4:
        print("Usage: python3 merge-image-map-json-files.py <json-file1> <json-file2> <output_file>")
        sys.exit(1)

def merge_json_files(file1, file2, output_file):
    """
    Merges two JSON files containing dictionaries and writes the merged content to an output file.

    Args:
        file1 (str): The path to the first JSON file.
        file2 (str): The path to the second JSON file.
        output_file (str): The path where the merged JSON file will be saved.

    Raises:
        FileNotFoundError: If one of the input files doesn't exist.
        ValueError: If either input file contains invalid JSON.
        TypeError: If either input file does not contain a dictionary.
        json.JSONDecodeError: If there is an error decoding JSON from the files.
        Exception: For any other unexpected errors.
    
    Returns:
        None: Writes the merged JSON data to the specified output file.
    """    
    try:
        # Load the JSON data from both files
        with open(file1, 'r') as f1:
            try:
                data1 = json.load(f1)
            except json.JSONDecodeError:
                raise ValueError(f"Error decoding JSON from {file1}")
        
        with open(file2, 'r') as f2:
            try:
                data2 = json.load(f2)
            except json.JSONDecodeError:
                raise ValueError(f"Error decoding JSON from {file2}")

        # Check if both data are dictionaries
        if not isinstance(data1, dict) or not isinstance(data2, dict):
            raise TypeError("Both JSON files should contain dictionaries.")

        # Merge the dictionaries (this will update data1 with data2, and keep all key-value pairs)
        merged_data = {**data1, **data2}

        # Write the merged data to a new JSON file
        with open(output_file, 'w') as out_file:
            json.dump(merged_data, out_file, indent=4)

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except ValueError as ve_error:
        print(f"ValueError: {ve_error}")
    except TypeError as te_error:
        print(f"TypeError: {te_error}")
    except json.JSONDecodeError as json_error:
        print(f"JSON Decode Error: {json_error}")
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

def main():
    check_arguments()
    mapping_file_1 = sys.argv[1]
    mapping_file_2 = sys.argv[2]
    output_file = sys.argv[3]
    merge_json_files(mapping_file_1, mapping_file_2, output_file)
    print(f"2 The JSON files {mapping_file_1}, {mapping_file_2} have been merged into {output_file}")

if __name__ == "__main__":
    main()
