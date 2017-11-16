import json
from nltk import word_tokenize
from quantities import units
from copy import deepcopy

class Recipe(object):
    
    def __init__(self, recipeInfo):      
        self.directions = Recipe.preprocessDirections(recipeInfo['Directions'])
        self.image = recipeInfo['Image']
        self.title = recipeInfo['Recipe']
        self.ingredients = recipeInfo['Ingredients']
        self.active = 0
        
        self.recipeInfo = recipeInfo

    def getDirections(self):
        return self.directions

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
            
    def isFraction(self, s):
        values = s.split('/')
        return len(values) == 2 and all(i.isdigit() for i in values)

    def getTimeRelatedDirections(self):
        units = ['minutes', 'hours', 'minute', 'hour', 'seconds']
        timeDirections = []
        for direction in self.getDirections():
            for token in word_tokenize(direction):
                if token in units and direction not in timeDirections:
                    timeDirections.append(direction)
        return timeDirections

    def getTemperatureRelatedDirections(self):
        units = ['degrees', 'celsius', 'fahrenheit', 'C', 'F', 'heat']
        tempDirections = []
        for direction in self.getDirections():
            for token in word_tokenize(direction):
                if token in units and direction not in tempDirections:
                    tempDirections.append(direction)
        return tempDirections


    def getTemperatureDirectionForQuery(self, query):
        tempDirections = self.getTemperatureRelatedDirections()
        matches = [0] * len(tempDirections)
        for i in range(len(tempDirections)):
            for token in word_tokenize(query):
                if token.lower() in tempDirections[i].lower().split():
                    matches[i] += 1

        applicableDirections = []
        for i in range(len(tempDirections)):
            if(matches[i] == max(matches)):
                applicableDirections.append(tempDirections[i])
        return applicableDirections

    def getTimeDirectionForQuery(self, query):
        timeDirections = self.getTimeRelatedDirections()
        matches = [0] * len(timeDirections)
        for i in range(len(timeDirections)):
            for token in word_tokenize(query):
                if token.lower() in timeDirections[i].lower().split():
                    matches[i] += 1

        applicableDirections = []
        for i in range(len(timeDirections)):
            if(matches[i] == max(matches)):
                applicableDirections.append(timeDirections[i])
        return applicableDirections

    def getIngredientsFromCurrentDirection(self):
        unitNames = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))] + [u for u, f in u.__dict__.items() if isinstance(f, type(units.deg))]
        unitNames.remove('in')
        unitNames.extend(['tablespoon', 'teaspoon', 'tsp', 'tbsp'])
        matches = [0] * len(self.ingredients)
        ingList = [deepcopy({'Val':"", 'Unit':"", 'Item':"", 'Text':""}) for i in range(len(self.ingredients))]
        
        for i in range(len(self.ingredients)):
            ingList[i]['Text'] = self.ingredients[i]
            for token in word_tokenize(self.ingredients[i]):
                if self.isFraction(token) or token.isnumeric():
                    ingList[i]['Val'] = token
                elif (token in unitNames) or (token[:-1] in unitNames):
                    ingList[i]['Unit'] = token
                else:
                    ingList[i]['Item'] = ingList[i]['Item'] + " " + token
                    if token in self.getCurrentDirection():
                        matches[i] += 1
                
        applicableIngredients = []
        for i in range(len(ingList)):
            if(matches[i] == max(matches)):
                applicableIngredients.append(ingList[i])
        
        return applicableIngredients

    def getIngredientFromQuery(self,query):
        results = []
        ingredients = self.getIngredientsFromCurrentDirection()
        for i in ingredients:
            if i['Item'] in query:
                results.append(i)
        return ingredients if len(results) == 0 else results
        

    def getInfo(self):
        return self.recipeInfo

    @staticmethod
    def preprocessDirections(directions):
        final = []
        directions = [d.replace('in.','in') for d in directions]
        directions = [d.replace('oz.','oz') for d in directions]
        for d in directions:
            for x in d.split('. '):
                final.append(x) if x.endswith('.') else final.append(x +'.')
        return final




        
