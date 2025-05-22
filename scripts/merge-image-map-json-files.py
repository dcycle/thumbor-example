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
    # Expecting at least 3 arguments: input1 input2 ... output
    if len(sys.argv) < 3:
        print("❌ Error: Not enough arguments.")
        print("Usage: python merge-image-map-json-files.py input1.json,input2.json,... output.json")
        sys.exit(1)

def merge_multiple_json_files(file_paths, output_file):
    """
    Merges multiple JSON files containing dictionaries into the first one and writes the result to an output file.

    Args:
        file_paths (list[str]): List of file paths to JSON files. The first file is the base.
        output_file (str): Path where the merged JSON will be saved.

    Raises:
        FileNotFoundError: If any file does not exist.
        ValueError: If any file contains invalid JSON.
        TypeError: If any file does not contain a dictionary.
        Exception: For any other unexpected errors.

    Returns:
        None
    """
    if not file_paths or len(file_paths) < 2:
        raise ValueError("At least two JSON file paths are required to perform a merge.")

    try:
        # Load and validate the base dictionary from the first file
        with open(file_paths[0], 'r') as f:
            try:
                merged_data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"Error decoding JSON from {file_paths[0]}")

        if not isinstance(merged_data, dict):
            raise TypeError(f"File {file_paths[0]} does not contain a JSON dictionary.")

        # Loop through the rest of the files and merge their dictionaries
        for path in file_paths[1:]:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"File not found: {path}")

            with open(path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    raise ValueError(f"Error decoding JSON from {path}")

                if not isinstance(data, dict):
                    raise TypeError(f"File {path} does not contain a JSON dictionary.")

                # Merge current dictionary into the base one
                merged_data.update(data)

        # Write the merged result to the output file (explicitly truncate first)
        with open(output_file, 'w') as out_file:
            out_file.truncate(0)  # Optional but explicit
            json.dump(merged_data, out_file, indent=4)

        # Remove all input files
        for path in file_paths:
            try:
                print(f"Attempting to delete: {path}")
                os.remove(path)
            except Exception as e:
                print(f"Warning: Failed to delete file {path}: {e}")

        print("!!! Success !!!")

    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    check_arguments()
    *input_files, output_file = sys.argv[1:]
    # First argument is comma-separated input file list
    input_files = sys.argv[1].split(',')
    # Second argument is the output file
    output_file = sys.argv[2]

    # Safety check
    if len(input_files) < 2:
        print("❌ Please provide at least two input files to merge.")
        sys.exit(1)

    print("input_files")
    print(input_files)
    print("output_file")
    print(output_file)

    merge_multiple_json_files(input_files, output_file)

if __name__ == "__main__":
    main()
