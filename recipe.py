import copy

from ingredient import *
from directions import *
# from RecipeFetcher import *

class Recipe(object):

    def __init__(self, recipe_name, ingredients=None, directions=None, methods=None, primary_cooking_method=None):
        self.recipe_name = recipe_name 
        # list of ingredients objects
        self.ingredients = ingredients
        # directions object
        self.directions = directions
        # primary cooking method
        # if primary_cooking_method == None:
        #     self.get_primary_cooking_method = self.get_primary_cooking_method(directions, methods)
        # # list of tools (str)
        # self.tools = tools
    
    def get_primary_cooking_method(self, directions, methods):
        print(directions)
        print(methods)
        return ""
        # for direction in directions:
        #     do = 'nothing'
    
    def to_healthy(self):
        # returns a copy of healthy version of recipe

        # make ingredients healthy
        healthy_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in healthy_ingredients:
            ingredient = ingredient.to_healthy()
        
        # make directions healthy
        healthy_directions = self.directions.to_healthy()

        # create new recipe object
        healthy_recipe = Recipe(healthy_ingredients, healthy_directions)

        return healthy_recipe

        

    def to_veg(self):
        # returns a copy of vegetarian version of recipe

        # make ingredients healthy
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg()
        

        # create new recipe object
        veg_recipe = Recipe(veg_ingredients, self.directions)

        return veg_recipe
