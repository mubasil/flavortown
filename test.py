from recipeswikia import RecipesWikia
from allrecipes import AllRecipes
import sys
import json
import time

scraper = AllRecipes()
link = 'http://allrecipes.com/recipe/'
i = 120200
recipes = []
while i < 120600:
    time.sleep(2)
    url = link + str(i)
    result = scraper.scrape(url)
    filename = 'recipes/' + result['Recipe'] + '.json'
    with open(filename, 'w') as outFile:
        json.dump(result, outFile)
    i += 1
    