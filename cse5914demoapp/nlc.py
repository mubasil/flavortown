import json
from watson_developer_cloud import NaturalLanguageClassifierV1 as NaturalLanguageClassifier



class NLC(object):
    def __init__(self):
        self.classifier = NaturalLanguageClassifier(
            username='c81a6f6c-ca40-4c31-9510-f7939f6332fb',
                password='VRzaHN6O4AAE')

    def classify(self, request):
        result = self.classifier.classify('ebd15ex229-nlc-23509', request)['classes'][0]
        if result['confidence'] >.90:
            return result['class_name']
        else:
            return None

