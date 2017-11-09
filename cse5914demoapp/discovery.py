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

    def query(self, ingredients):
        default_ingredients = ['water', 'salt', 'pepper']
        ingredients.extend(default_ingredients)
        self.ingredients = ingredients
        ingred_str = '|'.join([word for word in ingredients])
        query_str = "Ingredients:" + ingred_str
        qopts = {'query': query_str, 'count':1000}
        my_query = self.discovery.query('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', 
            '7844f79c-c259-4a3d-a2d8-2db7d18acd76', qopts)
        return self.processMatches(my_query['results'])
        
             
    #c:candidate ingredient list
    #p:provided ingredient list
    def isMember(self, c, p):
        misses = 0
        for ingredient in c:
            match = process.extractOne(ingredient, p)
            if match[1] < 90: misses = misses + 1
            if misses > 0: return False
        return True

    def isNearMember(self, c, p):
        misses = 0
        for ingredient in c:
            match = process.extractOne(ingredient, p)
            if match[1] < 90: misses = misses + 1
            if misses > 1: return False
        if misses == 1: return True
        else: return False

    #take the response from Watson and only keep recipes that are a good match
    def processExactMatches(self, results):
        trimmed_results = []
        for recipe in results:
            lst = recipe['Ingredients']
            if self.isMember(lst, self.ingredients): trimmed_results.append(recipe)
        return trimmed_results

    #take the response from Watson and only keep recipes that one ingredient from being a perfect match
    def processNearMatches(self, results):
        trimmed_results = []
        for recipe in results:
            lst = recipe['Ingredients']
            if self.isNearMember(lst, self.ingredients): trimmed_results.append(recipe)
        return trimmed_results

	#take the response from Watson and only keep recipes that one ingredient from being a perfect match
    def processMatches(self, results):
        trimmed_results_exact = []
        trimmed_results_near = []
        for recipe in results:
            lst = recipe['Ingredients']
            misses = 0
            for ingredient in lst:
                match = process.extractOne(ingredient, self.ingredients)
                if match[1] < 90: misses = misses + 1
            if misses == 1: trimmed_results_near.append(recipe)
            if misses == 0: trimmed_results_exact.append(recipe)
        return {'exact':trimmed_results_exact, 'near':trimmed_results_near}