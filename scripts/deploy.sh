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

echo ''
echo '-----'
echo 'About to create the thumbor_example_default_network network if it does'
echo 'not exist, echo 'because we need it to have a predictable name when we
echo 'try to connect other containers to it (for example testers).'
echo 'thumbor_example_default_network is then referenced in docker-compose.yml.'
echo 'See https://github.com/docker/compose/issues/3736.'
docker network ls | grep thumbor_example_default_network || docker network create thumbor_example_default_network

docker compose up -d --build

WEBSERVER=$(docker compose port webserver 80)
OPTIMIZATION=$(docker compose port image_optimization 80)

source ./scripts/lib/generate_thumbor_secure_url.source.sh

# Example unsafe URL part
unsafe_url_part="500x/webserver/large-image.jpg"
key=$THUMBOR_SECURITY_KEY

# Generate secure URL
secure_key=$(generate_thumbor_secure_url "$unsafe_url_part" "$key")

complete_secure_url="http://$OPTIMIZATION/$secure_key/$unsafe_url_part"

# Create a backup file and replace the image src in optimized.html with secure URL
sed -i.bak "s|image-server-domain-value-replace|http://$OPTIMIZATION|g" website-with-large-image/optimized.html

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
