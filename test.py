from scrape import RecipesWikia
import sys
import json

scraper = RecipesWikia(sys.argv[1])

result = scraper.scrape()
output = json.dumps(result, indent = 4, ensure_ascii=False).encode('utf-8')
print output