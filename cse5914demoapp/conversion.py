import urllib2
from bs4 import BeautifulSoup

class UnitConverter(object):
    
    @staticmethod
    def getConversion(request):
        query = urllib2.quote(request)
        url = "https://www.google.com/search?q=" + query
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)

        except urllib2.HTTPError, e:
            print e.fp.read()
        soup = BeautifulSoup(page, "html.parser")
        conversion = ()
        for identifier in ["_Cif", "_Aif"]:
            units = soup.find(id=identifier)
            units = [x for x in units.contents if x != ' ']
            val = units[0].get('value')
            label = units[1].find(selected="1").string
            unit = str(val) + " " + label
            conversion += (unit,)
        return conversion[0] + " = " + conversion[1]
