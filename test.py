from recipeswikia import RecipesWikia
from allrecipes import AllRecipes
import sys
import json
import time

scraper = AllRecipes()
link = 'http://allrecipes.com/recipe/'
i = 120090
recipes = []
while i < 120200:
    time.sleep(2)
    url = link + str(i)
    result = scraper.scrape(url)
    filename = 'recipes/' + result['Recipe'] + '.json'
    with open(filename,'w') as file:
        json.dump(result, file)
    i+=1