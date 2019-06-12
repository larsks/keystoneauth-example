#!/usr/bin/python

import json

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

auth = v3.Password(auth_url='http://localhost:5000/v3',
                   username='admin',
                   password='qwerty123',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')

# Get a session object. You can use a session to make authenticated requests.
sess = session.Session(auth=auth)

# For example, get a list of endpoints from keystone
print('## Getting all endpoints using Keystone REST API')
print()
endpoints = sess.get('http://localhost:5000/v3/endpoints')
for endpoint in endpoints.json()['endpoints']:
    print('{} {} {}'.format(endpoint['service_id'], endpoint['interface'],
                            endpoint['url']))

# The above makes a direct call to the Keystone REST API. We can also use the 
# Python PAI provided by the keystoneclient module:
print()
print('## Getting all endpoints using Python API')
print()
ks = client.Client(session=sess, interface='public')
for endpoint in ks.endpoints.list():
    print('{} {} {}'.format(endpoint.service_id, endpoint.interface,
                            endpoint.url))


# We can ask for a service endpoint by type. Using the REST API:
print()
print('## Looking for identity endpoints using the REST API')
print()
res = sess.get('http://localhost:5000/v3/services',
               params={'type': 'identity'})
service_id = res.json()['services'][0]['id']
res = sess.get('http://localhost:5000/v3/endpoints',
               params={'service_id': service_id, 'interface': 'public'})
print('Found identity enpdoint: {}'.format(res.json()['endpoints'][0]['url']))

print()
print('## Looking for identity endpoints using the Python API')
print()
service_id = ks.services.list(type='identity')[0].id
endpoints = ks.endpoints.list(service=service_id, interface='public')
print(endpoints)
