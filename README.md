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
    THUMBOR_SECURITY_KEY=your_thumbor_security_key_here
    ALLOW_UNSAFE_URL=False

Change your_thumbor_security_key_here to an arbitrary string.

Now, again, run

    ./scripts/deploy.sh

Now follow the instructions at [Letsencrypt HTTPS for Drupal on Docker, Dcycle Blog, Oct. 3, 2017](https://blog.dcycle.com/blog/170a6078/letsencrypt-drupal-docker/) and [Deploying Letsencrypt with Docker-Compose, Dcycle Blog, Oct. 6, 2017](https://blog.dcycle.com/blog/7f3ea9e1/letsencrypt-docker-compose/) to enable LetsEncrypt.

Now you can visit:

    https://images.example.com/3DW-hfnrLS8eunvhonsNJe6S79I=/500x/webserver/large-image.jpg

### Where does "3DW-hfnrLS8eunvhonsNJe6S79I=" come from?

As explained in the [Thumbor Security document](https://thumbor.readthedocs.io/en/latest/security.html), you can get this by running:

    source ./scripts/lib/generate_thumbor_secure_url.source.sh
    source .env
    unsafe_url_part=500x/webserver/large-image.jpg
    key=$THUMBOR_SECURITY_KEY
    generate_thumbor_secure_url "$unsafe_url_part" "$key"

In other words the individual security key (3DW-hfnrLS8eunvhonsNJe6S79I) is created by hashing the unsafe URL part (500x/webserver/large-image.jpg, or 500x/www.example.com/large-image.jpg) and the global security key (your_thumbor_security_key_here); the URL-specific security key will be different for each image.

Creating a map of unoptimized to optimized images
-----

Imagine you have a static website whose source code is all public. In such a case, you cannot store the Thumbor security key (in this example, `your_thumbor_security_key_here`), because it cannot be accessible to the public.

One solution might be:

* Every time your source code changes, have a a Jenkins job scan your website source code for all images.
* Use a script which uses the Thumbor security key as a secret, hidden from the public, to map all unoptimized images to optimized images.
* Create a json file with said mapping, which can be publicly available separately, or within, the website, which looks like this:

    {
        "/500x/webserver/large-image.jpg": "3DW-hfnrLS8eunvhonsNJe6S79I=",
        ...
    }

In this example:

* *500x* is the desired size of the optimized image, in this case 500 pixels wide;
* *webserver* is the name of the server as seen from within the Docker container hosting Thumbor. In real-world cases, this will be a domain such as `www.example.com`. In test scenarios, it can be the name of the Docker container as defined in `./docker-compose.yml`.
* *large-image.jpg* is the path to the unoptimized image.
* *3DW-hfnrLS8eunvhonsNJe6S79I* is the hash, as described in the section "Running this on a server", above.

Let us imagine that this JSON file is available somewhere such as `https://image-mapping.example.com/image-mapping.json`.

Now, the page `https://example.com/index.html` might reference an image such as `<img src="/large-image.jpg" />`. Instead of loading `./large-image.jpg` (which is unoptimized and might be very large) directly, the page might include a JavaScript file which fetches `https://image-mapping.example.com/image-mapping.json` and looks for whether the key `"/500x/example.com/large-image.jpg"` exists, and if it does, look for the value associated with that key, which is the token that should be used (let's say it's `3DW-hfnrLS8eunvhonsNJe6S79I`).

### If the token exists in the mapping file

Then replace:

    <img src="/large-image.jpg" />

with:

    <img src="https://images.example.com/3DW-hfnrLS8eunvhonsNJe6S79I/500x/example.com/large-image.jpg" />

### If the token does not exist

Then load the original file.

### How to generate the mapping file

The python script ./generate-image-map.py can be used to generate the mapping.

Here is how to use a Dockerized version of that script:

    export THUMBOR_SECURITY_KEY=your_thumbor_security_key_here
    ./generate-image-map.sh ./ webserver 500x ./unversioned/test.json

Updating your environment
-----

Run

    ./scripts/deploy.sh

In case of issues, you might want to confirm that the unversioned `./.env` file at the root of this directory has the same variables as the versioned `./.env-example`. For example, if you have deployed a previous version of this project which did not include the `THUMBOR_SECURITY_KEY` in `./env-example`, and you are upgrading, your `./.env` file might not contain `THUMBOR_SECURITY_KEY` and you will have to add it manually.

Destroying your environment
-----

    ./scripts/destroy.sh

Resources
-----
* [Use image CDNs to optimize images, by Jeremy Wagner et al., 2019-08-14, on web.dev](https://web.dev/articles/image-cdns)
* [How to install the Thumbor image CDN, by Katie Hempenius, 2019-08-14, on web.dev](https://web.dev/articles/install-thumbor)
* https://hub.docker.com/r/minimalcompact/thumbor/tags
* [Letsencrypt HTTPS for Drupal on Docker, Dcycle Blog, Oct. 3, 2017](https://blog.dcycle.com/blog/170a6078/letsencrypt-drupal-docker/)
* [Deploying Letsencrypt with Docker-Compose, Dcycle Blog, Oct. 6, 2017](https://blog.dcycle.com/blog/7f3ea9e1/letsencrypt-docker-compose/)

Images
-----

The images used herein come from the website Pexels:

* [Colonnade of the Mesudiye Medresesi by Mihman Duğanlı](https://www.pexels.com/photo/colonnade-of-the-mesudiye-medresesi-22475898/)
* [An older couple taking pictures in a chinese garden by Lu Pir](https://www.pexels.com/photo/an-older-couple-taking-pictures-in-a-chinese-garden-26626436/)
