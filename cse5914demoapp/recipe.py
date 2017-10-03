import json
import nltk
from quantities import units

class Recipe(object):
	
	def __init__(self, recipeInfo):      
		self.directions = Recipe.preprocessDirections(recipeInfo['Directions'])
		self.image = recipeInfo['Image']
		self.title = recipeInfo['Recipe']
		self.ingredients = recipeInfo['Ingredients']
		self.active = 0
		
		self.recipeInfo = recipeInfo

	def getCurrentDirection(self):
		return self.directions[self.active]

	def getSpecificDirection(self, index):
		self.active = index
		return self.getCurrentDirection()

	def goBack(self):
		if(self.active > 0):
			self.active -= 1
			return self.getCurrentDirection()
		else:
			return "That is the first step. " + self.getCurrentDirection()

	def goForward(self):
		if(self.active < len(self.directions) - 1):
			self.active += 1
			return self.getCurrentDirection()
		else:
			return "That is the last step. " + self.getCurrentDirection()

	def getIngredientFromCurrentDirection(self):
		unitNames = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))] + [u for u, f in u.__dict__.items() if isinstance(f, type(units.deg))]
		matches = [0] * len(self.ingredients)
		for i in range(len(self.ingredients)):
			for token in nltk.tokenize(self.ingredients[i]):
				if token not in unitNames:
					if token in self.getCurrentDirection():
						matches[i] += 1
		
		return self.ingredients[matches.index(max(matches))]

	def getInfo(self):
		return self.recipeInfo

	@staticmethod
	def preprocessDirections(directions):
		final = []
		directions = [d.replace('in.','in') for d in directions]
		for d in directions:
			for x in d.split('. '):
				final.append(x) if x.endswith('.') else final.append(x +'.')
		return final

''' TESTING DIRECTIONS PREPROCESSING METHOD		
json_data = open('exrecipe.json').read()
rec_dict = json.loads(json_data)
rec = Recipe(rec_dict)
for d in rec.directions:
	print d +"\n" '''

		
		
