#!/bin/bash
#
# Run ./generate-image-map.py in a Docker container
#
set -e

mkdir -p unversioned
Docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
  "export THUMBOR_SECURITY_KEY=$THUMBOR_SECURITY_KEY && export GENERATE_IMAGE_MAP_SHELL=/bin/sh && pip install python-dotenv && python3 /app/scripts/generate-image-map.py $1 $2 $3 $4"
