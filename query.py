import sys
import os
import json
import watson_developer_cloud
import itertools
from watson_developer_cloud import DiscoveryV1


class Discovery(object):
    def __init__(self):      
        self.discovery = DiscoveryV1(
          username='ff7c4fbe-e752-4c91-b99e-7f7db797e294',
          password='E3qe7yeI5Nrf',
          version='2017-09-01'
        )

    def query(self, ingreds):
        query_str = "Ingredients:" + ingred_str
        qopts = {'query': query_str, 'filter': query_str}
        return self.discovery.query('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', '7844f79c-c259-4a3d-a2d8-2db7d18acd76', qopts)

discovery = Discovery()
ingredients = ['garlic powder', 'paprika', 'popped popcorn', 'watermelon']
x = len(ingredients)
while x > 0:
  combo = itertools.combinations(ingredients,x)
  x -= 1
  recipe_found = False
  for c in combo:
    ingred_str = ','.join([word for word in c])
    my_query = discovery.query(ingred_str)
    if my_query['matching_results'] > 0:
      print(json.dumps(my_query, indent=2))
      recipe_found = True
  if recipe_found:
    break



