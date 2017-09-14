import urllib2 as url
from bs4 import BeautifulSoup

class AllRecipes:
    def __init__(self):
        self.url = None
        self.name = None
        self.ingredients = None
        self.directions = None
        self.image = None

    def scrape(self, link):
        self.url = url.urlopen(link)
        parser = BeautifulSoup(self.url, 'html.parser')
        self.name = self.get_name(parser)
        self.ingredients = self.get_ingredients(parser)
        self.directions = self.get_directions(parser)
        self.image = self.get_image(parser)
        return {
            'Recipe': self.name,
            'Image': self.image,
            'Ingredients': self.ingredients,
            'Directions': self.directions
        }


    def get_ingredients(self, page):
        supplies = page.find_all(class_='recipe-ingred_txt added')
        return [s.string for s in supplies]

    def get_directions(self, page):
        directions = page.find_all(class_='recipe-directions__list--item')
        return [d.string for d in directions if d.string is not None]

    def get_name(self, page):
        return page.find(class_="recipe-summary__h1").string

    def get_image(self,page):
        img = None
        if page.find(class_="rec-photo"):
            img = page.find(class_="rec-photo").get('src')
        return img
