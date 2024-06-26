#!/bin/bash
#
# Deploy the project.
#
set -e

docker pull minimalcompact/thumbor:6.7.5
docker pull httpd

if [ ! -f .env ]; then
  cp .env-example .env
fi

source .env

docker compose up -d --build

WEBSERVER=$(docker compose port webserver 80)
OPTIMIZATION=$(docker compose port image_optimization 80)

source ./scripts/lib/generate_thumbor_secure_url.source.sh

# Example unsafe URL part
unsafe_url_part="500x/webserver/large-image.jpg"
key=$THUMBOR_SECURITY_KEY

# Generate secure URL
echo "A"
echo "$unsafe_url_part"
echo "$key"
echo "B"
secure_key=$(generate_thumbor_secure_url "$unsafe_url_part" "$key")

complete_secure_url="http://$OPTIMIZATION/$secure_key/$unsafe_url_part"

# Create a backup file and replace the image src in optimized.html with secure URL
sed -i.bak "s|http://$OPTIMIZATION/unsafe/500x/webserver/large-image.jpg|$complete_secure_url|g" website-with-large-image/optimized.html

# Remove the backup file
rm website-with-large-image/optimized.html.bak

echo " => "
echo " => All done!"
echo " => "
echo " => You can now visit your site at"
echo " => "
echo " => http://$WEBSERVER"
echo " => "
echo " => And you can see an optimized and secure image at "
echo " => "
echo " => $complete_secure_url"
echo " => "
