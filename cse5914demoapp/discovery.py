import sys
import os
import json
import watson_developer_cloud
from watson_developer_cloud import DiscoveryV1
from fuzzywuzzy import process


class Discovery(object):
    def __init__(self):      
        self.discovery = DiscoveryV1(
          username='ff7c4fbe-e752-4c91-b99e-7f7db797e294',
          password='E3qe7yeI5Nrf',
          version='2017-09-01'
        )

    def query(self, ingred_str):
        query_str = "Ingredients:" + ingred_str
        qopts = {'query': query_str}
        return self.discovery.query('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', '7844f79c-c259-4a3d-a2d8-2db7d18acd76', qopts)
    #determine if an ingredient string roughly matches
    #an element in the list of provided ingredients
    def isMember(self, s, l):
        result = process.extractOne(s, l)
        return result[1] >= 80
    #take the response from Watson and only keep recipes that are a good match
    #results: List of recipe dictionaries 
    #discovery.query(...)['results']
    def processResponse(self, results):
        trimmed_results = []
        for recipe in results:
            good_candidate = True
            lst = recipe['Ingredients']
            for s in lst:
                if not self.isMember(s, ingredients):
                    good_candidate = False
                    break
            if good_candidate: trimmed_results.append(recipe)
        return trimmed_results   