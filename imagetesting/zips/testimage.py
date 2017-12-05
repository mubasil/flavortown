from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
import json
'''
vr = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')
vr.delete_classifier('foodtest_30840956')

with open('test.zip', 'rb') as img:
    param = {'classifier_ids':["foodtest_30840956"]}
    params = json.dumps(param)
    print(json.dumps(vr.classify(images_file=img, parameters=params), indent=2))
'''

file = open('curl.txt', 'wx')

with open('ingredients.txt') as f:
    lines = f.read().splitlines()

file.write("curl -X POST ")

for line in lines:
    underscored = line.replace(' ', '_')
    file.write('--form "' + underscored + '_positive_examples=@' +line+ '.zip" ')
    
file.write('--form "name=foodtest" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers?api_key=7b851fccf7f17a35fc7569a5dad6e1eb4f650f70&version=2016-05-20"')
file.close()
