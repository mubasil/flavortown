from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json
import sys
from discovery import Discovery 

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

ingredientsList = []
recipes = {}
selectedRecipe = {}


#takes in a list of ingredients, returns list of possible recipes
def getExactRecipes(ingredients):
	discovery = Discovery()
	my_query = discovery.query(ingredients)
	return my_query

#takes in a list of ingredients, returns list of possible recipes
def getNearRecipes(ingredients):
    discovery = Discovery()
    my_query = discovery.query(ingredients, False)
    return my_query


#takes in an image file and returns a list of ingredients in the image
def processImage(imagefile):

	ingredientList = [{'ingredient':''}]
	
	#TODO logic
	
	return ingredientList


#takes in a text query, returns a text and voice answer
def answerQuery(query):

	answer = {'text':'', 'voice':''}
	
	#TODO logic
	
	return answer



if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 5000))

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/processImage', methods=['POST'])
def getIngredientsFromImage():
	#imagefile = flask.request.files.get('imagefile', '')
	imagefile = ""
	ingredientList = processImage(imagefile)
	return jsonify(ingredientList)
	
@app.route('/getRecipes', methods=['GET'])
def getRecipesFromIngredientsList():
	global ingredientsList
	recipeList = getExactRecipes(ingredientsList)
	return jsonify(recipeList)
	
@app.route('/postIngredients', methods=['POST'])
def postIngredients():
	global ingredientsList
	content = request.get_json(silent=True)
	ingredientsList = content
	return jsonify(ingredientsList)
	
@app.route('/selectRecipe', methods=['POST'])
def selectRecipe():
	global selectedRecipe
	content = request.get_json(silent=True)
	selectedRecipe = content
	return jsonify(selectedRecipe)
	
@app.route('/getAnswer', methods=['POST'])
def getAnswerToQuestion():
	content = request.get_json(silent=True)
	query = content['query']
	request = answerQuery(query)
	return jsonify(request)
	
@app.route('/getSelected', methods=['GET'])
def getSelectedRecipe():
	return jsonify(selectedRecipe)
	
@app.route('/page/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)