from recipeswikia import RecipesWikia
from allrecipes import AllRecipes
import sys
import json
import time

scraper = AllRecipes()
link = 'http://allrecipes.com/recipe/'
i = 121513
recipes = []
while i < 122000:
    print i
    url = link + str(i)
    result = scraper.scrape(url)
    filename = 'recipes2/' + result['Recipe'] + '.json'
    with open(filename, 'w') as outFile:
        json.dump(result, outFile)
    i += 1
    time.sleep(1.5)
    