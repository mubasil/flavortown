import sys
import os
import json
import watson_developer_cloud
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import TextToSpeechV1 as TextToSpeech


class SpeechText(object):
    def __init__(self):      
        self.STT = SpeechToText(
          username='824801e9-c8af-4ecd-ac9a-bbc001cf7769',
          password='2Ug6krjqdA8R'
        )
		self.TTS = TextToSpeech(
          username='159ac011-2033-457d-bd66-f5bddc650685',
          password='aVtZSYPCAe8L'
        )

    def transcribe_audio(audio_file):
        return STT.recognize(audio_file, content_type=’audio/wav’)

    def speak_text(text):
		return TTS.recognize(audio_file, content_type=’audio/wav’)