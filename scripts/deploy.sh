#!/bin/bash
#
# Deploy the project.
#
set -e

docker pull minimalcompact/thumbor:6.7.5
docker pull httpd

docker compose up -d --build

WEBSERVER=$(docker compose port webserver 80)
OPTIMIZATION=$(docker compose port image_optimization 80)

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
