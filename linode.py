import re
import json
import requests

# Generate a Linode personal access token with full access to domains using the newe Linode manager
access_token = 'put your token here'

def get_domain(name):
    '''Gets the domain with the given name.'''
    url = 'https://api.linode.com/v4/domains'
    headers = {
        'Authorization': 'Bearer %s' % access_token,
        'X-Filter': '{ "domain": "%s" }' % name
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    domains = response.json()['data']
    return next((d for d in domains if d['domain'] == name), None)


def get_records(domain_id, name):
    '''Gets the TXT records with the given name for the given domain.'''
    url = 'https://api.linode.com/v4/domains/%i/records' % domain_id
    headers = {
        'Authorization': 'Bearer %s' % access_token,
        'X-Filter': '{ "name": "%s" }' % name
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    records = response.json()['data']
    return [r for r in records if r['type'] == 'TXT' and r['name'] == name]


def delete_record(domain_id, record_id):
    '''Deletes a record for the given top domain.'''
    url = 'https://api.linode.com/v4/domains/%i/records/%i' % (domain_id, record_id)
    headers = { 'Authorization': 'Bearer %s' % access_token }

    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def create_record(domain_id, name, value):
    '''Creates a TXT record with the given name and value for the given top domain.'''
    url = 'https://api.linode.com/v4/domains/%i/records' % domain_id
    headers = { 'Authorization': 'Bearer %s' % access_token }
    body = {
        'type': 'TXT',
        'name': name,
        'target': value,
        'ttl_sec': 300
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def parse_top_domain(domain_name):
    '''Parses the top-most domain name from an arbitrarily deep subdomain.'''
    return re.match(r'^(?:.+\.)?(.+\..+)$', domain_name).group(1)


def generate_challenge_name(domain_name):
    '''Generates the name for the ACME challenge TXT record, which depends on the domain name.'''
    top_domain = parse_top_domain(domain_name)

    if domain_name != top_domain:
        return '_acme-challenge.' + domain_name[:-len('.' + top_domain)]

    return '_acme-challenge'