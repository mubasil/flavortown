from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
import json

vr = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')
print(json.dumps(vr.list_classifiers()))
'''
file = open('curl.txt', 'wx')

with open('ingredients.txt') as f:
    lines = f.read().splitlines()

file.write("curl -X POST ")

for line in lines:
    underscored = line.replace(' ', '_')
    file.write('--form "' + underscored + '_positive_examples=@' +line+ '.zip" ')
    
file.close()
'''