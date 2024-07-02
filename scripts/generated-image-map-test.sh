#!/bin/bash
#
# Test the script that generates an unoptimized-to-optimized image map.
#
set -e

if [ ! -f ./app/website-with-large-image/unversioned-image-mapping.json ]; then
  echo "./app/website-with-large-image/unversioned-image-mapping.json not found. Please run the script that generates it (./scripts/generate-image-map.sh) first."
  exit 1
fi

echo "Confirming that all safe url path and signtured generated in /app/website-with-large-image/unversioned-image-mapping.json are accessible"

# Note that the second argument is the host and port of the server that will be
# used to test the URLs. In the case of our test it is 0.0.0.0:8705, however
# instead of passing 0.0.0.0:8705 (8705 is the port defined in
# docker-compose.yml by which a client computer can access port 80 within the
# image_optimization docker container) to the script, we will pass
# "image_optimization", because in the context of the Docker container,
# 0.0.0.0:8705 is accessible through the name "image_optimization" (see the
# docker-compose.yml file), and this requires that our Docker script be able to
# access the same network as is used by our docker-compose.yml file.
output=$(docker run -v $(pwd):/app \
  --network thumbor_example_default_network \
  --rm --entrypoint /bin/sh python:3-alpine -c \
  "pip install requests && python3 /app/scripts/generated-image-map-test.py /app/website-with-large-image/unversioned-image-mapping.json ")

# Check the content of the output
if echo "$output" | grep -q "400"; then
  echo "Some tests failed. Here's the detailed output:"
  echo "$output"
  exit 1
elif echo "$output" | grep -q "Err"; then
  echo "Not expecting the string Err to appear in the output. Here's the detailed output:"
  echo "$output"
  exit 1
else
  echo "All tests passed!"
fi
