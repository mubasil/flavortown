from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, send_file
from StringIO import StringIO
import atexit
import cf_deployment_tracker
import os
import json
import sys
import wave
from nltk import word_tokenize
from discovery import Discovery 
from speechtext import SpeechText
from recipe import Recipe
from nlc import NLC
from conversion import UnitConverter
from youtube import Youtube
from quantities import units
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
#from imageRecognizer import ImageClassifier

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

ingredientsList = []
recipes = {}
selectedRecipe = {}

speech_text = SpeechText()


#takes in a list of ingredients, returns list of possible recipes
def getRecipes(ingredients):
    discovery = Discovery()
    my_query = discovery.query(ingredients)
    return my_query

#takes in a list of ingredients, returns list of possible recipes
def getExactRecipes(ingredients):
    discovery = Discovery()
    my_query = discovery.query(ingredients)
    return my_query

#takes in a list of ingredients, returns list of possible recipes
def getNearRecipes(ingredients):
    discovery = Discovery()
    my_query = discovery.query(ingredients)
    return my_query


#takes in an image file and returns a list of ingredients in the image
def processImage(imagefile):

    ingredientList = [{'ingredient':''}]
    
    #imageClassifier = ImageClassifier()
    
    #ingredientList = imageClassifier.classify(imagefile)
    
    return ingredientList


#takes in a text query, returns a text and voice answer
def answerQuery(query):
    global selectedRecipe
    answer = {'text':"", 'voice':''}
    
    nlc = NLC()
    my_class = ""
    if query:
        if query.endswith('?'):
            query = query[:-1]
        my_class = nlc.classify(query)

    #possible options:
    
    if my_class == "current":
        #Read the current step
        answer['text'] = selectedRecipe.getCurrentDirection()
    elif my_class == "next":    
        #Read the next step
        answer['text'] = selectedRecipe.goForward()
    elif my_class == "previous":
        #Read the previous step 
        answer['text'] = selectedRecipe.goBack()
    elif my_class == "specific":
        #Read a specific step (query~"What was the first step?")
        words = query.split()
        index = -1  
        key_words = {
            'first': 0,
            'start': 0,
            'beginning': 0,
            'second': 1,
            'third': 2,
            'fourth': 3,
            'fifth': 4,
            'sixth': 5,
            'seventh': 6,
            'eighth': 7,
            'ninth': 8,
            'tenth': 9,
            'eleventh': 10,
            'twelfth': 11,
            'last': len(selectedRecipe.directions) - 1,
            'end': len(selectedRecipe.directions) - 1,
            'finish': len(selectedRecipe.directions) - 1
        }
        for word in words:
            if word in key_words:
                index = key_words[word]

        if index > len(selectedRecipe.directions) - 1 or index < 0:
            answer['text'] = "The recipe does not have that many steps" 
        else:
            answer['text'] = selectedRecipe.getSpecificDirection(index)      
    
    elif my_class == "ingredients":
        #Find out current ingredient (query~"How much of that?")
        relaventIngredients = selectedRecipe.getIngredientFromQuery(query)
        answer['text'] = relaventIngredients.pop()['Text']
        for ing in relaventIngredients:
            answer['text'] = answer['text'] + " and " + ing['Text']
    
    elif my_class == "conversion":
        unitNames = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))] + [u for u, f in u.__dict__.items() if isinstance(f, type(units.deg))]
        unitNames.extend(['tablespoon', 'teaspoon', 'tsp', 'tbsp'])
        unitsFound = []

        for token in word_tokenize(query):
            if (token in unitNames) or (token[:-1] in unitNames):
                if(token != 'in' and token != 'do' and token != 'use'):
                    unitsFound.append(token)
        app.logger.info(unitsFound)
        if(len(unitsFound) == 1):
            for ing in selectedRecipe.getIngredientFromQuery(query):
                conversionQuery = "What is " + ing['Val'] + " " + ing['Unit'] + " in " + unitsFound[0]
                app.logger.info(conversionQuery)
                if answer['text']:
                    answer['text'] = answer['text'] + " and "
                answer['text'] = answer['text'] + UnitConverter.getConversion(conversionQuery)
        elif(len(unitsFound) > 1):
            answer['text'] = UnitConverter.getConversion(query)
        elif(len(unitsFound) == 0):
            answer['text'] = "Sorry, I don't know how to convert that."
    
    elif my_class == "howto":
        answer['text'] = Youtube.getVideo(query) 

    elif my_class == "temperature":
        answer['text'] = selectedRecipe.getTemperatureDirectionForQuery(query)
        
    elif my_class == "time":
        answer['text'] = selectedRecipe.getTimeDirectionForQuery(query)
    else:
        answer = {'text':"Sorry, I didn't get that.", 'voice':''}
    
    
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
    
@app.route('/getExactRecipes', methods=['GET'])
def getExactRecipesFromIngredientsList():
    global ingredientsList
    recipeList = getExactRecipes(ingredientsList)
    return jsonify(recipeList)
    
@app.route('/getRecipes', methods=['GET'])
def getRecipesFromIngredientsList():
    global ingredientsList
    recipeList = getRecipes(ingredientsList)
    return jsonify(recipeList)
    
@app.route('/getNearRecipes', methods=['GET'])
def getNearRecipesFromIngredientsList():
    global ingredientsList
    recipeList = getNearRecipes(ingredientsList)
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
    selectedRecipe = Recipe(content)
    return jsonify(selectedRecipe.recipeInfo)
    
@app.route('/getSelected', methods=['GET'])
def getSelected():
    global selectedRecipe
    return jsonify(selectedRecipe.recipeInfo)
    
@app.route('/getAnswer', methods=['POST'])
def getAnswerToQuestion():
    content = request.get_json(silent=True)
    query = content['query']
    request = answerQuery(query)
    return jsonify(request)
    
@app.route('/ask', methods=['POST'])
def ask():
    content = request.get_json(silent=True)
    answer = answerQuery(content['textInfo'])
    return jsonify(answer)

@app.route('/stt', methods=['POST'])
def stt():
    global speech_text
    content = request.files['file']
    txt = speech_text.transcribe_audio(content)
    return jsonify(txt)
    
@app.route('/tts', methods=['POST'])
def tts():
    global speech_text
    content = request.get_json(silent=True)
    audio = speech_text.speak_text(content['textInfo'])
    buf = StringIO()
    
    orig = wave.open(audio)
    
    file = wave.open(buf, 'w')
    file.setparams(orig.getparams())
    file.writeframes(audio)
    file.close()
    
    
    response = make_response(buf.getvalue())
    buf.close()
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
    return response

@app.route('/api/speech-to-text/token')
def getSttToken():
    authorization = Authorization(username='824801e9-c8af-4ecd-ac9a-bbc001cf7769', password='2Ug6krjqdA8R')
    return authorization.get_token(url=SpeechToText.default_url)
    
@app.route('/page/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
