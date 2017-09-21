import sys
import os
import json
import watson_developer_cloud
from watson_developer_cloud import DiscoveryV1

environment_id = '0a15c836-8ec9-41ca-a33b-93a9d63dae8d'
configuration_id = 'be19de2d-41e6-4240-919d-fc3ac86dc4e7'
collection_id = '7844f79c-c259-4a3d-a2d8-2db7d18acd76'

discovery = DiscoveryV1(
  username='ff7c4fbe-e752-4c91-b99e-7f7db797e294',
  password='E3qe7yeI5Nrf',
  version='2017-09-01'
)
ingredients = ['garlic powder', 'paprika', 'popped popcorn']
ingred_str = ','.join([i for i in ingredients])
query_str = "Ingredients:" + ingred_str
qopts = {'query': query_str}
my_query = discovery.query('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', '7844f79c-c259-4a3d-a2d8-2db7d18acd76', qopts)
print(json.dumps(my_query['results'], indent=2))

