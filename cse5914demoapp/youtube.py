import urllib2
from bs4 import BeautifulSoup

class Youtube(object):  

    @staticmethod
    def getVideo(phrase):
        query = urllib2.quote(phrase)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        vid =soup.find(attrs={'class':'yt-uix-tile-link'})
        vid_url = 'https://www.youtube.com' + vid['href']
        vid_code = vid_url[vid_url.index('=')+1:]
        return '''<iframe width="240" height="135" src="https://www.youtube.com/embed/''' + str(vid_code) + '''" frameborder="0" allowfullscreen></iframe>'''
