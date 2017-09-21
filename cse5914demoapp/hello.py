from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json
import sys
import watson_developer_cloud
from watson_developer_cloud import DiscoveryV1

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
def getRecipes(ingredients):
	discovery = DiscoveryV1(    
        username='ff7c4fbe-e752-4c91-b99e-7f7db797e294',
        password='E3qe7yeI5Nrf',
        version='2017-09-01'
	)
	ingred_str = ','.join([i for i in ingredients])
	query_str = "Ingredients:" + ingred_str
	qopts = {'query': query_str}
	my_query = discovery.query('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', '7844f79c-c259-4a3d-a2d8-2db7d18acd76', qopts)
	return my_query['results']



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
	recipeList = getRecipes(ingredientsList)
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