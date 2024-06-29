import subprocess
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Assuming the .env file is in the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

def generate_thumbor_secure_url(unsafe_url_part, security_key):
    script_path = os.path.abspath('./scripts/lib/generate_thumbor_secure_url.source.sh')
    command = f'source {script_path} && generate_thumbor_secure_url "{unsafe_url_part}" "{security_key}"'

    try:
        result = subprocess.check_output(command, shell=True, executable='/bin/bash')
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
