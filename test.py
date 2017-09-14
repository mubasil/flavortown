from recipeswikia import RecipesWikia
from allrecipes import AllRecipes
import sys
import json

scraper = AllRecipes()
link = 'http://allrecipes.com/recipe/'
i = 120000
recipes = []
while i < 120050:
    url = link + str(i)
    result = scraper.scrape(url)
    filename = 'recipes/' + result['Recipe'] + '.json'
    with open(filename,'w') as file:
        json.dump(result, file)
    i+=1