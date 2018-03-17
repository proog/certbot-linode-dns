# Certbot DNS-01 challenge hooks for Linode

A set of scripts that facilitate DNS-01 validation when used with Certbot's manual mode.

The DNS-01 challenge works by generating a validation string that must be placed in a specially named TXT record, i.e. `_acme-challenge.example.com`. These scripts use [Linode's v4 API](https://developers.linode.com/v4/introduction) to add and remove TXT records for domains whose DNS is hosted by Linode.

It works like this:

1. Look up the parent domain of the (sub-)domain being validated
2. Delete any existing TXT records with the same name as the one needed for the challenge
3. Create a new TXT record using the requested name and validation string
4. Wait 20 minutes to allow Linode to update (according to them, changes are applied every quarter hour)
5. *Certbot performs validation and acquires certs*
6. Clean up by deleting the TXT record

## Prerequisites

 - Python 3, pip and [pipenv](https://docs.pipenv.org/#install-pipenv-today) (unless you're okay with installing [requests](http://docs.python-requests.org/) globally)
 - A Linode [personal access token](https://cloud.linode.com/profile/tokens) with *full access* to the *domains* category

## Installation

1. Clone the repository
2. Run `pipenv install` inside
3. Paste your personal access token near the top of `linode.py` (you'll know where)

## Usage

When running Certbot in manual mode, specify `dns` as the only preferred challenge, `pipenv_auth.sh` for the auth hook, and `pipenv_cleanup.sh` for the cleanup hook.

Example:

```
certbot certonly --manual --preferred-challenges=dns \
    --manual-auth-hook /path/to/pipenv_auth.sh \
    --manual-cleanup-hook /path/to/pipenv_cleanup.sh \
    -d secure.example.com
```

For testing, add the `--dry-run` flag.

The two shell scripts are thin wrappers that merely run the Python scripts in the pipenv-created virtual environment. If you prefer not to use pipenv, you can directly specify `auth.py` and `cleanup.py` instead. They will use whatever `python3` resolves to on your system. Remember to install `requests` globally as well.

## Caveats

DNS is is black magic. The time it takes for DNS changes to propagate can vary wildly. If you find that validation is failing, try increasing the waiting period near the end of `auth.py`.

Linode's v4 API is (at the time of writing) still in early access, though I expect little to change in the few features used by this software.
