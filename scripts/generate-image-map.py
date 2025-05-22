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
from itertools import islice
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

# Smart Cropping¶
# If the smart mode of thumbor has been specified in the uri (by the /smart portion of it),
# thumbor will use it’s smart detectors to find focal points.
# thumbor comes pre-packaged with two focal-point detection algorithms: facial and feature.
# First it tries to identify faces and if it can’t find any, it tries to identify 
# features (more on that below).
# https://thumbor.readthedocs.io/en/latest/detection_algorithms.html
    options = {'smart': True, 'image_url': path}
    if width != "":
        options['width'] = width
    if height != "":
        options['height'] = height
    return crypto.generate(**options)

def chunked_iterator(iterable, batch_size):
    """Yield successive batches of items from an iterator."""
    it = iter(iterable)
    while True:
        chunk = list(islice(it, batch_size))
        if not chunk:
            break
        yield chunk

def update_mapping_data(images_directory, server_domain, sizes, mapping_file, security_key, batch_size=100):
    """
    Updates a JSON mapping file with secure tokens for image resizing endpoints.

    This function scans all image files within the specified directory, processes them in batches, and
    generates secure tokens for each specified image size. The mapping is saved to a JSON file, allowing
    secure, dynamic resizing or delivery of images via a server.

    Parameters:
        images_directory (str):
            Path to the directory containing images to be mapped.

        server_domain (str):
            The base domain or URL prefix used to construct secure image URLs (e.g., "localhost:4000/media").

        sizes (str):
            A comma-separated string specifying image dimensions (e.g., "800x,x600,400x300").
            Each entry can be:
                - WxH (e.g., "800x600")
                - Wx (width only, e.g., "800x")
                - xH (height only, e.g., "x600")

        mapping_file (str):
            Path to the JSON file where the mapping data will be stored. If the file doesn't exist, it is created.

        security_key (str):
            A secret key used to generate secure tokens (e.g., HMAC or hash-based).

        batch_size (int, optional):
            Number of images to process in a single batch to avoid memory/resource issues. Default is 100.

    Notes:
        - Only image files with extensions (.jpg, .jpeg, .png, .gif, .bmp, .tiff) are processed.
        - If an image mapping already exists in the file, new sizes are added without overwriting existing ones.
        - This function is suitable for large image folders by using incremental processing.

    Raises:
        JSONDecodeError: If the mapping file exists but contains invalid JSON.

    Example:
        update_mapping_data(
            images_directory='./media',
            server_domain='localhost:4000/media',
            sizes='800x,x600,400x300',
            mapping_file='./mapping.json',
            security_key='my-secret',
            batch_size=100
        )
    """
    # Step 1: Load existing mapping
    with open(mapping_file, 'r+') as f:
        try:
            mapping_data = json.load(f)
        except json.JSONDecodeError:
            mapping_data = {}

        # Step 2: Gather all image paths
        image_paths = []
        for root, _, files in os.walk(images_directory):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

        # Step 3: Process in batches
        for batch in chunked_iterator(image_paths, batch_size):
            for image_path in batch:
                relative_path = os.path.relpath(image_path, images_directory)
                map_key = f"/{relative_path}"
                if map_key not in mapping_data:
                    mapping_data[map_key] = {}

                for size in extract_size(sizes):
                    width, height = extract_width_height(size)
                    secure_token = generate_secure_token(width, height, security_key, f"{server_domain}/{relative_path}")
                    mapping_data[map_key][f"{width}x{height}"] = secure_token

        # Step 4: Save final mapping
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
