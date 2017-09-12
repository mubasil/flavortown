from scrape import RecipesWikia
import sys
import json

scraper = RecipesWikia(sys.argv[1])

result = scraper.scrape()
print json.dumps(result,indent = 4)