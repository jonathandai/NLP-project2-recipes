import nltk
import re

VALID_UNITS = ['teaspoon', 'teaspoons', 'tablespoon', 'tablespoons', 'pound', 'pounds', 'ounce', 'ounces', 'cup', 'cups']

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
        self.name = name
        self.quantity = quantity
        self.unit = unit

    # def to_healthy(self):
    #     # convert ingredient to healthy substitute
    #     pass
    
    def to_veg(self):
        # convert ingredient to veg substitutde
        pass
    

