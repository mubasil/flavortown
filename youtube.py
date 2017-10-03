import urllib
import urllib2
from bs4 import BeautifulSoup

class YoutubeSearch(object):

    def __init__(self, phrase):
        query = urllib.quote(phrase)
        self.url = "https://www.youtube.com/results?search_query=" + query

    def search(self):
        response = urllib2.urlopen(self.url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        vid =soup.find(attrs={'class':'yt-uix-tile-link'})
        return 'https://www.youtube.com' + vid['href']
