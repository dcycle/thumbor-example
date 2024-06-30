#
# Usage:
#
# export THUMBOR_SECURITY_KEY=your_thumbor_security_key_here
# [optional] export GENERATE_IMAGE_MAP_SHELL=/bin/sh (default: /bin/bash)
# ./scripts/generate-iamge-map.sh \
#    /path/to/images/directory \
#    you.server.with.unoptimized.images.example.com \
#    300x300 \ # the desired size of the optimized images
#    /path/to/output/image-map.json
#
# After running this script, /path/to/output/image-map.json will
# contain a JSON object with the mapping of the original image URLs, like this:
#
#    {
#        "/500x/webserver/large-image.jpg": "3DW-hfnrLS8eunvhonsNJe6S79I=",
#        ...
#    }
#

import subprocess
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Assuming the .env file is in the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# This script needs to know which shell to use. By default it will use /bin/bash
# but if you are running this in Alpine linux for example, /bin/bash is not
# available, so you are prepend the call to this script with
# export GENERATE_IMAGE_MAP_SHELL=/bin/sh as can be seen in
# ./scripts/generate-image-map.sh.
shell_to_use = os.getenv('GENERATE_IMAGE_MAP_SHELL') if os.getenv('GENERATE_IMAGE_MAP_SHELL') else "/bin/bash";

def generate_thumbor_secure_url(unsafe_url_part, security_key):
    script_path = os.path.abspath('./scripts/lib/generate_thumbor_secure_url.source.sh')
    command = f'source {script_path} && generate_thumbor_secure_url "{unsafe_url_part}" "{security_key}"'

    try:
        result = subprocess.check_output(command, shell=True, executable=shell_to_use)
        secure_key = result.decode('utf-8').strip()
        return secure_key
    except subprocess.CalledProcessError as e:
        print(f"Error running shell script: {e}")
        return None

def main():
    # Check if all arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python3 ./scripts/generate-image-map2.py <images_directory> <server_domain> <size> <output_json_file>")
        sys.exit(1)

    images_directory = sys.argv[1]
    server_domain = sys.argv[2]
    size = sys.argv[3]
    output_json_file = sys.argv[4]

    # Check if the images directory exists
    if not os.path.isdir(images_directory):
        print(f"Error: Directory '{images_directory}' does not exist.")
        sys.exit(1)

    print(f"Directory '{images_directory}' exists. Generating image map...")

    # Ensure the output JSON file exists or create it as an empty object {}
    output_json_path = Path(output_json_file)
    if not output_json_path.exists():
        output_json_path.write_text("{}")

    security_key = os.getenv('THUMBOR_SECURITY_KEY')
    if not security_key:
        print("Error: THUMBOR_SECURITY_KEY environment variable is not set.")
        sys.exit(1)

    # Iterate over images in the directory
    image_map = {}
    for filename in os.listdir(images_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Processing image: {filename}")
            # Construct the unsafe URL part
            unsafe_url_part = f"{size}/{server_domain}/{filename}"
            # Generate secure URL using shell script
            securekey = generate_thumbor_secure_url(unsafe_url_part, security_key)
            if securekey:
                # Store in the image map dictionary
                image_map[unsafe_url_part] = securekey

    # Write the image map dictionary to the output JSON file
    with open(output_json_file, 'w') as f:
        json.dump(image_map, f, indent=2)

    print(f"Image map successfully generated and saved to {output_json_file}")

if __name__ == "__main__":
    main()
