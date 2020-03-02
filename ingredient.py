import nltk
import re
from nltk import pos_tag

VALID_UNITS = ['teaspoon', 'teaspoons', 'tablespoon', 'tablespoons', 'pound', 'pounds', 'ounce', 'ounces', 'cup', 'cups']

healthy_substitutes = {
    'butter' : '½ cup coconut oil',
    'egg' : '3 egg whites',
    'sugar' : '½ cup agave',
    'mayonnaise' : 'light mayonnaise',
    'heavy cream' : 'pureed beans',
    'bread crumbs' : 'oatmeal',
    'flour' : 'almond flour',
    'White Rice' : 'Brown Rice',
    'pasta' : 'zoodles (Zucchini Noodles)'
  }

unhealthy_substitutes = {
    'Brown Rice' : 'White Rice',
    'whole wheat pasta' : 'pasta',
    'light mayonnaise' : 'mayonnaise',
    'brown sugar' : 'sugar',
    'olive oil' : 'butter',
    'grapeseed oil' : 'corn oil',
    'coconut oil' : 'corn oil',
    'whole wheat bread' : 'white bread',
    'oatmeal' : 'cereal',
    'milk' : 'whole milk',
    'sweet potato' : 'potato'
}
class Ingredient(object):

    def __init__(self, ingredient_string):
        # TODO: Deal with parsing for standarized units
        if '(' in ingredient_string and ')' in ingredient_string:
            substring = ingredient_string[ingredient_string.find("(")+1:ingredient_string.find(")")]
            substring_tokens = substring.split(' ')
            quantity = substring_tokens[0]
            unit = substring_tokens[1]

            # extract ingredient name
            tokens = ingredient_string.split(' ')
            new_start_index = tokens.index(substring_tokens[1]+')') + 2
            name_tokens = tokens[new_start_index:]
            name =  ' '.join(name_tokens)
        else:
            text = nltk.word_tokenize(ingredient_string)
            tagged_text = nltk.pos_tag(text)
            # get quantity
            index = 0
            for i in range(len(tagged_text)):
                word = tagged_text[i]
                if word[1] != 'CD':
                    index = i
                    break
            tokens = ingredient_string.split(' ')
            quantity = ' '.join(tokens[:index])
            unit = ""
            name = ""
            if index == len(tokens)-1:
                quantity = tokens[0]
                name = tokens[1]
            else:
                global VALID_UNITS
                if tokens[index].lower() in VALID_UNITS:
                    unit = tokens[index]
                    name = ' '.join(tokens[index+1:])
                else:
                    name = ' '.join(tokens[index:])

        prep = ""
        if ", " in name:
            name_split_comma = name.split(',', 1)
            name = name_split_comma[0]
            prep = name_split_comma[1]

        descriptors = []
        if len(name.split()) > 1:
            for i, name in enumerate(name.split()):
                if i != len(name.split())+1:
                    descriptors.append(name)



        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.prep = prep
        self.descriptor = descriptors

    def __repr__(self):
        return "name: " + self.name + " // unit: "+ self.unit + " // quantity: " + self.quantity + " // prep: " + self.prep + "\n"

    def to_healthy(self):
        # convert ingredient to healthy substitute
        for key in healthy_substitutes:
            if key in self.name:
                self.name = healthy_substitutes[key]

    def to_veg(self, meats_to_substitute):
        for meat, substitute in meats_to_substitute.items():
            if meat in self.name:
                self.name = substitute
                return
