# export THUMBOR_SECURITY_KEY=your_thumbor_security_key_here
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
#        "large-image.jpg": "3DW-hfnrLS8eunvhonsNJe6S79I=/500x/webserver/large-image.jpg",
#        ...
#    }
#

import os
import sys
import json
from dotenv import load_dotenv
from libthumbor import CryptoURL

# Assuming the .env file is in the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# We are passing size argument as 200x or 200x300 or x400.
# We need to exctract width and height from size.
def extract_width_height(size):
    # Default values
    width = None
    height = None

    if size:
        parts = size.split('x')
        if len(parts) == 2:
            if parts[0]:
                width = int(parts[0])
            if parts[1]:
                height = int(parts[1])
        elif len(parts) == 1 and parts[0]:
            if parts[0].isdigit():
                width = int(parts[0])
            else:
                height = int(parts[0])

    return width, height

# We are generating secure url part.
# Ex:- /v4N0hVTSDSUhTyej8TYfSK2BLfw=/200x0/smart/webserver/img_20230202_121358_113.jpg
def generate_secure_token(width, height, key, path):
    crypto = CryptoURL(key)

    options = {
        'smart': True,
        'image_url': path
    }

    if width is not None:
        options['width'] = width
    if height is not None:
        options['height'] = height

    encrypted_url = crypto.generate(**options)
    return encrypted_url

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 generate-image-map.py <images_directory> <server_domain> <size> <mapping_file>")
        sys.exit(1)

    images_directory = sys.argv[1]
    server_domain = sys.argv[2]
    size = sys.argv[3]
    mapping_file = sys.argv[4]

    # Read security key from environment variable
    security_key = os.getenv('THUMBOR_SECURITY_KEY')
    if not security_key:
        print("Error: THUMBOR_SECURITY_KEY environment variable is not set.")
        sys.exit(1)

    # Ensure the images directory exists
    if not os.path.isdir(images_directory):
        print(f"Error: Images directory '{images_directory}' not found.")
        sys.exit(1)

    # Ensure mapping_file path is valid
    mapping_file_dir = os.path.dirname(mapping_file)
    if not os.path.isdir(mapping_file_dir):
        print(f"Directory for mapping file '{mapping_file_dir}' does not exist.")
        sys.exit(1)

    # Ensure mapping_file exists or create an empty JSON object
    if os.path.isfile(mapping_file):
        print(f"Mapping file '{mapping_file}' exists. Emptying its contents...")
        with open(mapping_file, 'w') as f:
            json.dump({}, f)
    else:
        print(f"Mapping file '{mapping_file}' does not exist. Creating an empty JSON file...")
        with open(mapping_file, 'w') as f:
            json.dump({}, f)

    width, height = extract_width_height(size)

    # Prepare to update the mapping JSON
    with open(mapping_file, 'r+') as f:
        mapping_data = json.load(f)

        # Iterate over images in the directory
        for root, _, files in os.walk(images_directory):
            for file in files:
                # Check if file is an image (ignoring case)
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                    image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(image_path, images_directory)
                    secure_token = generate_secure_token(width, height, security_key, f"{server_domain}/{relative_path}")
                    mapping_data[f"/{relative_path}"] = secure_token

        # Write updated mapping data to the file
        f.seek(0)
        json.dump(mapping_data, f, indent=2)
        f.truncate()

    print(f"Image mapping successfully updated in {mapping_file}")

if __name__ == "__main__":
    main()
