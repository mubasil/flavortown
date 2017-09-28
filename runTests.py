from hello import getRecipes, processImage, answerQuery

# Preliminary test cases


# getRecipes tests

# print out a recipe list for manual checking
#def display_recipe_list(recipeList):	
#	for recipe in recipeList:
#		for field in recipe:
#			print(field + '\n')
#		print('\n')


def getRecipes_has_result():
	sampleIngredientsList = ['apple', 'banana']
	assert getRecipes(sampleIngredientsList) is not None

def getRecipes_from_apple():
	sampleIngredientsList = ['apple']
	recipeList = getRecipe(sampleIngredientsList)
	for recipe in recipeList:
		assert 'apple' in recipe.get('Ingredients')
	display_recipe_list(recipeList)

# processImage tests

def processImage_has_result():
	sampleImageFile = "apple.jpg"
	assert processImage(sampleImageFile) is not None

def processImage_identify_apple():
	sampleImageFile = "apple.jpg"
	ingredientsList = processImage(sampleImageFile)
	assert 'apple' in ingredientsList
	assert len(ingredientsList) == 1 # check no extra ingredients


# answerQuery tests

def answerQuery_has_result():
	sampleQuery = "How do I start?"
	answer = answerQuery(sampleQuery)
	assert answer is not None
	print answer.get('text')


getRecipes_has_result() 
