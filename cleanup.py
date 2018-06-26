#!/usr/bin/env python

import os
import linode

access_token = os.getenv('LINODE_ACCESS_TOKEN')

if access_token is not None:
    linode.access_token = access_token

challenge_domain = os.environ['CERTBOT_DOMAIN']

top_domain = linode.parse_top_domain(challenge_domain)
domain = linode.get_domain(top_domain)

if domain is None:
    raise Exception("Domain %s not found" % top_domain)

print('Using %s with id %i' % (domain['domain'], domain['id']))

record_name = linode.generate_challenge_name(challenge_domain)
records = linode.get_records(domain['id'], record_name)

for record in records:
    print('Deleting existing TXT record %s with id %i' % (record['name'], record['id']))
    linode.delete_record(domain['id'], record['id'])

print('Done')
