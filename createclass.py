import csv
import json
import os


classifiers = []
recipeClasses = ["Asian", "Mexican", "Italian"]

for recipeClass in recipeClasses:
    directory = os.path.join(os.getcwd(), recipeClass)
	
    for filename in os.listdir(directory):

        with open(os.path.join(directory, filename)) as fileinfo:
            data = json.loads(fileinfo.read())
            allIngredients = ""
            for datum in data['Ingredients']:
                allIngredients = allIngredients + " " + datum
            classifiers.append({'query':allIngredients, 'classifier':recipeClass})
			
writer = csv.writer(open('train.csv', 'w'))
for row in classifiers:
	writer.writerow([unicode(row['query']).encode("utf-8"), unicode(row['classifier']).encode("utf-8")])