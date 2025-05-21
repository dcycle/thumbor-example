#!/bin/bash
#
# Run ./merge-image-map-json-files.py in a Docker container
#

docker run -v $(pwd):/app --rm --entrypoint /bin/sh python:3-alpine -c \
  "python3 /app/scripts/merge-image-map-json-files.py $1 $2 $3"
