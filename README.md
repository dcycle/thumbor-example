[![CircleCI](https://dl.circleci.com/status-badge/img/gh/dcycle/thumbor-example/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/dcycle/thumbor-example/tree/master)

Thumbor example
-----

Run ./scripts/deploy.sh to get an example of how to use [Thumbor](https://www.thumbor.org/) to optimize images for any website.

Running this on a server
-----

Make sure images.example.com points to your server, for example 1.2.3.4.

Then once on your server run:

    DOMAIN=images.example.com
    docker pull minimalcompact/thumbor:6.7.5
    docker run -d \
      -e ALLOWED_SOURCES="['example.org', 'www.example.org']" \
      -e "VIRTUAL_HOST=$DOMAIN" \
      -e "LETSENCRYPT_HOST=$DOMAIN" \
      -e "LETSENCRYPT_EMAIL=$DOMAIN" \
      --expose 80 --name thumbor \
      minimalcompact/thumbor:6.7.5

Then figure out what network your container is in:

    docker container inspect thumbor

The network will look like "bridge" or "example_bridge".

    NETWORK=bridge


    DOMAIN=images.example.com


Resources
-----
* [Use image CDNs to optimize images, by Jeremy Wagner et al., 2019-08-14, on web.dev](https://web.dev/articles/image-cdns)
* [How to install the Thumbor image CDN, by Katie Hempenius, 2019-08-14, on web.dev](https://web.dev/articles/install-thumbor)
* https://hub.docker.com/r/minimalcompact/thumbor/tags
* The image used here is from Mihman Duğanlı and [comes from Pexels](https://www.pexels.com/photo/colonnade-of-the-mesudiye-medresesi-22475898/)
* [Letsencrypt HTTPS for Drupal on Docker, Dcycle Blog, Oct. 3, 2017](https://blog.dcycle.com/blog/170a6078/letsencrypt-drupal-docker/)
* [Deploying Letsencrypt with Docker-Compose, Dcycle Blog, Oct. 6, 2017](https://blog.dcycle.com/blog/7f3ea9e1/letsencrypt-docker-compose/)
