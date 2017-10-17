import sys
import os
import json
import watson_developer_cloud
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import TextToSpeechV1 as TextToSpeech


class SpeechText(object):
    def __init__(self):      
		self.STT = SpeechToText(username='824801e9-c8af-4ecd-ac9a-bbc001cf7769', password='2Ug6krjqdA8R')
		self.TTS = TextToSpeech(username='159ac011-2033-457d-bd66-f5bddc650685', password='aVtZSYPCAe8L')

    def transcribe_audio(self, audio_file):
        return self.STT.recognize(audio_file, content_type='audio/wav')['results'][0]['alternatives'][0]['transcript']

    def speak_text(self, text):
		return self.TTS.synthesize(text, accept='audio/wav')