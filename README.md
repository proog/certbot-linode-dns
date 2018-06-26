# Certbot DNS-01 challenge hooks for Linode

Until an official Linode DNS plugin is available, here's a set of scripts that facilitate DNS-01 validation when used with Certbot's manual mode.

The DNS-01 challenge works by generating a validation string that must be placed in a specially named TXT record, i.e. `_acme-challenge.example.com`. These scripts use [Linode's v4 API](https://developers.linode.com/api/v4) to add and remove TXT records for domains whose DNS is hosted by Linode.

It works like this:

1. Look up the parent domain of the (sub-)domain being validated
2. Delete any existing TXT records with the same name as the one needed for the challenge
3. Create a new TXT record using the requested name and validation string
4. Wait 20 minutes to allow Linode to update (according to them, changes are applied every quarter hour)
5. *Certbot performs validation and acquires certs*
6. Clean up by deleting the TXT record

## Prerequisites

- A Linode [personal access token](https://cloud.linode.com/profile/tokens) with *full access* to the *domains* category
- Python 2/3 and [requests](http://docs.python-requests.org/). If you don't want to install requests globally you can use [pipenv](https://docs.pipenv.org/#install-pipenv-today) and the included wrapper scripts. Alternatively, there's a [Docker image](https://hub.docker.com/r/proog/certbot-linode-dns/) available.

## Installation

1. Clone the repository
2. Run `pipenv install` inside
3. Set the `LINODE_ACCESS_TOKEN` environment variable or paste your access token near the top of `linode.py`

Alternatively, there's a [Docker image](https://hub.docker.com/r/proog/certbot-linode-dns/) available based on the official Certbot image.

## Usage

When running Certbot in manual mode, specify `dns` as the only preferred challenge, `pipenv_auth.sh` for the auth hook, and `pipenv_cleanup.sh` for the cleanup hook. For testing, add the `--dry-run` flag.

Example:

```sh
LINODE_ACCESS_TOKEN=mytoken certbot certonly \
    --manual --preferred-challenges=dns \
    --manual-auth-hook /path/to/pipenv_auth.sh \
    --manual-cleanup-hook /path/to/pipenv_cleanup.sh \
    -d secure.example.com
```

The two shell scripts are thin wrappers that run the Python scripts in the pipenv-created virtual environment. If you prefer not to use pipenv, you can directly specify `auth.py` and `cleanup.py` instead. They will use whatever `/usr/bin/env python` resolves to on your system. Remember to install `requests` globally as well.

Example with Docker (the image automatically adds the appropriate options):

```sh
docker run --rm -it -e LINODE_ACCESS_TOKEN=mytoken \
    proog/certbot-linode-dns certonly -d secure.example.com
```

## Caveats

DNS is is black magic. The time it takes for DNS changes to propagate can vary wildly. If you find that validation is failing, try increasing the waiting period near the end of `auth.py`.

Note that due to the way Certbot processes output from hook scripts, the output will only be available *after* each script has finished. Because of this, the auth hook script may seem to hang with no output for the duration of the waiting period. This is expected behavior.
