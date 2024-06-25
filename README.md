[![CircleCI](https://dl.circleci.com/status-badge/img/gh/dcycle/thumbor-example/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/dcycle/thumbor-example/tree/master)

Thumbor example
-----

Run ./scripts/deploy.sh to get an example of how to use [Thumbor](https://www.thumbor.org/) to optimize images for any website.

Running this on a server
-----

Make sure images.example.com points to your server, for example 1.2.3.4.

Then once on your server run:

    git clone https://github.com/dcycle/thumbor-example.git thumbor
    cd thumbor
    ./scripts/deploy.sh

Then edit the ~/thumbor/.env file and put in there:

    VIRTUAL_HOST=images.example.com
    ALLOWED_SOURCES=['example.com', 'www.example.com']

Now, again, run

    ./scripts/deploy.sh

Now follow the instructions at [Letsencrypt HTTPS for Drupal on Docker, Dcycle Blog, Oct. 3, 2017](https://blog.dcycle.com/blog/170a6078/letsencrypt-drupal-docker/) and [Deploying Letsencrypt with Docker-Compose, Dcycle Blog, Oct. 6, 2017](https://blog.dcycle.com/blog/7f3ea9e1/letsencrypt-docker-compose/) to enable LetsEncrypt.

Now you can visit:

    https://images.example.com/unsafe/500x/example.com/path/to/large.jpg

Updating your environment
-----

Run

    ./scripts/deploy.sh

In case of issues, you might want to confirm that the unversioned `./.env` file at the root of this directory has the same variables as the versioned `./.env-example`. For example, if you have deployed a previous version of this project which did not include the `THUMBOR_SECURITY_KEY` in `./env-example`, and you are upgrading, your `./.env` file might not contain `THUMBOR_SECURITY_KEY` and you will have to add it manually.

Destroying your environment
-----

    docker compose down -v
    rm .env

Thumbor Service Security Implementation.
-----
* Kindly refer [Thumbor Security doc](https://thumbor.readthedocs.io/en/latest/security.html)

Resources
-----
* [Use image CDNs to optimize images, by Jeremy Wagner et al., 2019-08-14, on web.dev](https://web.dev/articles/image-cdns)
* [How to install the Thumbor image CDN, by Katie Hempenius, 2019-08-14, on web.dev](https://web.dev/articles/install-thumbor)
* https://hub.docker.com/r/minimalcompact/thumbor/tags
* The image used here is from Mihman Duğanlı and [comes from Pexels](https://www.pexels.com/photo/colonnade-of-the-mesudiye-medresesi-22475898/)
* [Letsencrypt HTTPS for Drupal on Docker, Dcycle Blog, Oct. 3, 2017](https://blog.dcycle.com/blog/170a6078/letsencrypt-drupal-docker/)
* [Deploying Letsencrypt with Docker-Compose, Dcycle Blog, Oct. 6, 2017](https://blog.dcycle.com/blog/7f3ea9e1/letsencrypt-docker-compose/)
