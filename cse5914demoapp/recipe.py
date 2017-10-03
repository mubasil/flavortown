import json
import nlkt
from quantities import units

class Recipe(object):
    def __init__(self, recipeInfo):      
        self.directions = recipeInfo['Directions']
		self.image = recipeInfo['Image']
		self.title = recipeInfo['Recipe']
		self.ingredients = recipeInfo['Ingredients']
		self.active = 0
		
		self.recipeInfo = recipeInfo

    def getCurrentDirection(self):
        return directions[active]
	
	def getSpecificDirection(self, index):
		active = index
		return self.getCurrentDirection()
	
	def goBack(self):
		if(active > 0)
			active -= 1
			return self.getCurrentDirection()
		else
			return "That is the first step. " + self.getCurrentDirection()
             
	def goForward(self):
		if(active < len(directions) - 1)
			active += 1
			return self.getCurrentDirection()
		else
			return "That is the last step. " + self.getCurrentDirection()
	
	def getIngredientFromCurrentDirection(self)
		
		units = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))] + [u for u, f in u.__dict__.items() if isinstance(f, type(units.deg))]
		matches = [0] * len(ingredients)
		for i in range(len(ingredients))
			for token in nltk.tokenize(ingredients[i])
				if token not in units
					if token in self.getCurrentDirection()
						matches[i] += 1
		
		return ingredients[matches.index(max(matches))]
	
	def getInfo(self)
		return recipeInfo