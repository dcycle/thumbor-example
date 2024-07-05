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

def check_arguments():
    if len(sys.argv) != 5:
        print("Usage: python3 generate-image-map.py <images_directory> <server_domain> <size> <mapping_file>")
        sys.exit(1)

def load_environment_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    security_key = os.getenv('THUMBOR_SECURITY_KEY')
    if not security_key:
        print("Error: THUMBOR_SECURITY_KEY environment variable is not set.")
        sys.exit(1)
    return security_key

def validate_images_directory(images_directory):
    if not os.path.isdir(images_directory):
        print(f"Error: Images directory '{images_directory}' not found.")
        sys.exit(1)

def initialize_mapping_file(mapping_file):
    mapping_file_dir = os.path.dirname(mapping_file)
    if not os.path.isdir(mapping_file_dir):
        print(f"Directory for mapping file '{mapping_file_dir}' does not exist.")
        sys.exit(1)
    if os.path.isfile(mapping_file):
        print(f"Mapping file '{mapping_file}' exists. Emptying its contents...")
        with open(mapping_file, 'w') as f:
            json.dump({}, f)
    else:
        print(f"Mapping file '{mapping_file}' does not exist. Creating an empty JSON file...")
        with open(mapping_file, 'w') as f:
            json.dump({}, f)

# We are passing size argument as 200x or 200x300 or x400.
# We need to exctract width and height from size.
def extract_width_height(size):
    width = ""
    height = ""
    parts = size.split('x')
    if len(parts) == 2:
        width = int(parts[0]) if parts[0] else ""
        height = int(parts[1]) if parts[1] else ""
    elif len(parts) == 1 and parts[0]:
        if parts[0].isdigit():
            width = int(parts[0])
        else:
            height = int(parts[0])
    return width, height

def extract_size(sizes):
    return sizes.split(',')

# We are generating secure url part.
# Ex:- /v4N0hVTSDSUhTyej8TYfSK2BLfw=/200x0/smart/webserver/img_20230202_121358_113.jpg
def generate_secure_token(width, height, key, path):
    crypto = CryptoURL(key)
    options = {'smart': True, 'image_url': path}
    if width != "":
        options['width'] = width
    if height != "":
        options['height'] = height
    return crypto.generate(**options)

def update_mapping_data(images_directory, server_domain, sizes, mapping_file, security_key):
    with open(mapping_file, 'r+') as f:
        mapping_data = json.load(f)
        for root, _, files in os.walk(images_directory):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                    image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(image_path, images_directory)
                    mapping_data[f"/{relative_path}"] = {}
                    for size in extract_size(sizes):
                        width, height = extract_width_height(size)
                        secure_token = generate_secure_token(width, height, security_key, f"{server_domain}/{relative_path}")
                        mapping_data[f"/{relative_path}"].update(
                          {
                            f"{width}x{height}": secure_token,
                          }
                        )
        f.seek(0)
        json.dump(mapping_data, f, indent=2)
        f.truncate()

def main():
    check_arguments()
    images_directory = sys.argv[1]
    server_domain = sys.argv[2]
    sizes = sys.argv[3]
    mapping_file = sys.argv[4]

    security_key = load_environment_variables()
    validate_images_directory(images_directory)
    initialize_mapping_file(mapping_file)

    update_mapping_data(images_directory, server_domain, sizes, mapping_file, security_key)

    print(f"Image mapping successfully updated in {mapping_file}")

if __name__ == "__main__":
    main()
