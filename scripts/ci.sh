#!/bin/bash
#
# Deploy the project.
#
set -e

./scripts/deploy.sh

echo "We need to wait awhile before accessing the resource"

sleep 10

echo "Confirming that we can get an image securely from webserver - encoded signature for image size (500x)"

curl -I http://0.0.0.0:8705/3DW-hfnrLS8eunvhonsNJe6S79I=/500x/webserver/large-image.jpg | grep 200

echo "Confirming that we cannot get an image from encoded signature and varying size (400x)"

curl -I -v http://0.0.0.0:8705/3DW-hfnrLS8eunvhonsNJe6S79I=/400x/webserver/large-image.jpg | grep 400

echo "Confirming that we cannot get an image from unsafe url"

curl -I http://0.0.0.0:8705/unsafe/500x/webserver/large-image.jpg | grep 400

echo "Confirming that we cannot get an image from other sources"

curl -I http://0.0.0.0:8705/unsafe/500x/webserver_no_access/large-image.jpg | grep 400

echo "Confirming that we can generate an unoptimized-to-optimized image map"

source .env
export THUMBOR_SECURITY_KEY="$THUMBOR_SECURITY_KEY"
./scripts/generate-image-map.sh ./app/website-with-large-image webserver 200x ./app/unversioned/image-map.json

echo "All done with tests!"
