import copy

from Ingredient import *
from Instructions import *

class Recipe(object):

    def __init__(self, recipe_name, ingredients=None, instructions=None):
        self.recipe_name = recipe_name 
        # list of ingredients objects
        self.ingredients = ingredients
        # instructions object
        self.instructions = instructions
        # list of tools (str)
        # self.tools = tools
    
    def to_healthy(self):
        # returns a copy of healthy version of recipe

        # make ingredients healthy
        healthy_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in healthy_ingredients:
            ingredient = ingredient.to_healthy()
        
        # make instructions healthy
        healthy_instructions = self.instructions.to_healthy()

        # create new recipe object
        healthy_recipe = Recipe(healthy_ingredients, healthy_instructions)

        return healthy_recipe

        

    def to_veg(self):
        # returns a copy of vegetarian version of recipe

        # make ingredients healthy
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg()
        

        # create new recipe object
        veg_recipe = Recipe(veg_ingredients, self.instructions)

        return veg_recipe

