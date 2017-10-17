import hello
from hello import getExactRecipes, getNearRecipes, processImage, answerQuery 
from recipe import Recipe
import json

# Preliminary test cases


# getRecipes tests

# print out a recipe list for manual checking
#def display_recipe_list(recipeList):    
#    for recipe in recipeList:
#        for field in recipe:
#            print(field + '\n')
#        print('\n')


def getRecipes_has_result():
    sampleIngredientsList = ['apple', 'banana']
    assert getExactRecipes(sampleIngredientsList) is not None

def getRecipes_from_apple():
    sampleIngredientsList = ['apple']
    recipeList = getExactRecipes(sampleIngredientsList)
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

#recipe class tests
def createRecipeWorks():
    file = open("exrecipe.json", "r")
    data = json.loads(file.read())
    recipe = Recipe(data)
    assert recipe is not None
    
def getDirectionsFromRecipeWorks():
    file = open("exrecipe.json", "r")
    data = json.loads(file.read())
    recipe = Recipe(data)
    assert recipe.getCurrentDirection() == data['Directions'][0]
    
def moveCursorRecipeWorks():
    file = open("exrecipe.json", "r")
    data = json.loads(file.read())
    recipe = Recipe(data)

    directions = Recipe.preprocessDirections(data['Directions'])

    forward = recipe.goForward()
    print(forward)
    print(directions[1])

    assert forward == directions[1]
    assert recipe.goBack() == directions[0]



# answerQuery tests

def set_example_recipe():
    json_data = open('exrecipe.json').read()
    rec_dict = json.loads(json_data)
    hello.selectedRecipe = Recipe(rec_dict)

def answerQuery_has_result():
    sampleQuery = "How do I start?"
    answer = answerQuery(sampleQuery)
    assert answer is not None
    print answer.get('text')


getRecipes_has_result() 

createRecipeWorks()
getDirectionsFromRecipeWorks()
moveCursorRecipeWorks()

#set_example_recipe()
#answerQuery_has_result()


