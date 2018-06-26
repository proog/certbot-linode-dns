FROM certbot/certbot:latest

RUN pip install requests

COPY *.py linode/

ENTRYPOINT [ "certbot", "--manual", "--preferred-challenges", "dns", "--manual-auth-hook", "linode/auth.py", "--manual-cleanup-hook", "linode/cleanup.py" ]
