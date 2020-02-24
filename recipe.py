import copy

from ingredient import *
from instructions import *

class recipe(object):

    def __init__(self, ingredients=None, instructions=None):
        # list of ingredients objects
        self.ingredients = ingredients
        # instructions object
        self.instructions = instructions
    
    def to_healthy(self):
        # returns a copy of healthy version of recipe

        # make ingredients healthy
        healthy_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in healthy_ingredients:
            ingredient = ingredient.to_healthy()
        
        # make instructions healthy
        healthy_instructions = self.instructions.to_healthy()

        # create new recipe object
        healthy_recipe = recipe(healthy_ingredients, healthy_instructions)

        return healthy_recipe

        

    def to_veg(self):
        # returns a copy of vegetarian version of recipe

        # make ingredients healthy
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg()
        

        # create new recipe object
        veg_recipe = recipe(veg_ingredients, self.instructions)

        return veg_recipe

