from recipeswikia import RecipesWikia
from allrecipes import AllRecipes
import sys
import json

scraper = None
if 'allrecipes' in sys.argv[1]:
    scraper = AllRecipes(sys.argv[1])
else:
    scraper = RecipesWikia(sys.argv[1])

result = scraper.scrape()
recipe = json.dumps(result, indent = 4, ensure_ascii=False).encode('utf-8')
print recipe