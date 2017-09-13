import urllib2 as url
from bs4 import BeautifulSoup

class RecipesWikia:
    def __init__(self, link):
        self.url = url.urlopen(link)
        self.name = None
        self.ingredients = None
        self.directions = None
        self.image = None

    def scrape(self):
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
        ingredients = []
        supplies = page.find(id='Ingredients').parent.next_sibling.next_sibling
        for bullet in supplies.contents:
            line = ' '.join([c.string.strip() for c in bullet.contents if c != ' '])
            ingredients += [line[:-1]] if line.endswith(' ') else [line]
        return ingredients

    def get_directions(self, page):
        directions = []
        steps = page.find(id='Directions').parent.next_sibling.next_sibling
        for bullet in steps.contents:
            line = ' '.join([c.string.strip() for c in bullet.contents if c != ' '])
            directions += [line[:-1]] if line.endswith(' ') else [line]
        return directions

    def get_name(self, page):
        return page.find(class_="page-header__title").string

    def get_image(self,page):
        img = None
        if page.find(class_="image image-thumbnail"):
            img = page.find(class_="image image-thumbnail").get('href')
        elif page.find(class_="floatright"):
            img = page.find(class_="floatright").contents[0].get('src')
        return img



