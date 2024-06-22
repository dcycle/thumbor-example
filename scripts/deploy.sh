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

# Generate secure Thumbor URL
generate_thumbor_secure_url() {
  local unsafe_part="$1"
  local security_key="$THUMBOR_SECURITY_KEY"

  # Calculate HMAC-SHA1 signature with base 64 encoded
  local signature=$(echo -n "$unsafe_part" | openssl dgst -sha1 -hmac "$security_key" -binary | base64 | tr '+/' '-_' )
  echo "$signature"  # Return the value instead of echoing it
}

# Example unsafe URL part
unsafe_url_part="500x/webserver/large-image.jpg"

# Generate secure URL
secure_url=$(generate_thumbor_secure_url "$unsafe_url_part")

complete_secure_url="http://$OPTIMIZATION/$secure_url/$unsafe_url_part"

echo " => "
echo " => All done!"
echo " => "
echo " => You can now visit your site at"
echo " => "
echo " => http://$WEBSERVER"
echo " => "
echo " => And you can see an optimized image at "
echo " => "
echo " => http://$OPTIMIZATION/unsafe/500x/webserver/large-image.jpg"
echo " => "

# Replace image src in optimized.html with secure URL
sed -i "" "s|http://$OPTIMIZATION/unsafe/500x/webserver/large-image.jpg|$complete_secure_url|g" website-with-large-image/optimized.html

