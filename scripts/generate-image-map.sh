#!/bin/bash
#
# Run ./generate-image-map.py in a Docker container
#
set -e

mkdir -p unversioned
OPTIMIZATION=$(docker compose port image_optimization 80)

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
  "export THUMBOR_SECURITY_KEY=$THUMBOR_SECURITY_KEY && pip install python-dotenv libthumbor && python3 /app/scripts/generate-image-map.py $1 $2 $3 $4 $OPTIMIZATION"
