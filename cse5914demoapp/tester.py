from recipe import Recipe
import json

data = json.loads(open("exrecipe.json","r").read())
recipe = Recipe(data)

print(recipe.goForward())
print(recipe.goForward())

print(recipe.getIngredientFromCurrentDirection())