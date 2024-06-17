#!/bin/bash
#
# Deploy the project.
#
set -e

./scripts/deploy.sh

echo "Confirming that we can get an image from webserver"

curl -I http://0.0.0.0:8705/unsafe/500x/webserver/large-image.jpg | grep 200

echo "Confirming that we cannot get an image from other sources"

curl -I http://0.0.0.0:8705/unsafe/500x/webserver_no_access/large-image.jpg | grep 200 && exit 1

echo "All done with tests!"