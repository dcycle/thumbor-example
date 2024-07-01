import os
import sys
import subprocess
import json
import requests
from urllib.parse import quote

# pip install requests // install requests if you haven't installed it.
# python3 ./scripts/generated-image-map-test.py unversioned/image-map.json 0.0.0.0:8705
def test_urls(output_json_file, server_domain):
    try:
        with open(output_json_file, 'r') as f:
            image_map = json.load(f)
    except json.decoder.JSONDecodeError:
        print(f"Error: JSON file '{output_json_file}' is empty or invalid.")
        return

    if not image_map:
        print(f"Error: JSON file '{output_json_file}' is empty.")
        return

    all_accessible = True  # Flag to track if all URLs are accessible

    for unsafe_url_part, secure_url in image_map.items():
        full_url = f"http://{server_domain}{quote(secure_url)}"
        try:
            response = requests.get(full_url)
            if response.status_code != 200:
                all_accessible = False  # Set flag to False if any exception occurs
                print(f"ERROR: URL {full_url} returned status code {response.status_code}")
                break  # Stop testing further URLs upon encountering a non-200 status code
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL {full_url}: {str(e)}")
            all_accessible = False  # Set flag to False if any exception occurs
    if all_accessible:
        print("---- Success: All Images are accessible. ----")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generated-image-map-test.py <output_json_file> <server_domain>")
        sys.exit(1)

    output_json_file = sys.argv[1]
    server_domain = sys.argv[2]

    if not os.path.isfile(output_json_file):
        print(f"Error: File '{output_json_file}' does not exist.")
        sys.exit(1)

    test_urls(output_json_file, server_domain)

if __name__ == "__main__":
    main()
