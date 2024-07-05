#!/bin/bash
#
# Destroy the project.
#
set -e

docker compose down -v
rm -f .env
rm -f ./website-with-large-image/unversioned-image-mapping.json
rm -f ./website-with-large-image/this-unversioned-large-image-is-purposefully-not-mapped.jpg
docker network rm thumbor_example_default_network 2>/dev/null || true
