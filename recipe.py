import copy
import re 
from Ingredient import *
from directions import *
from recipe import *
# from RecipeFetcher import *

class Recipe(object):

    def __init__(self, recipe_name, url=None, ingredients=None, directions=None, tools=None, methods=None, nutrition=None, primary_cooking_method=None):
        self.recipe_name = recipe_name 
        self.url = url
        # list of ingredients objects
        self.ingredients = ingredients
        # directions object
        self.directions = directions
        self.tools = tools 
        self.methods = methods
        self.nutrition = nutrition
        self.primary_cooking_method = primary_cooking_method
    
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
        
    def map_meat_to_cooking_method(self, directions, methods):
        '''
        returns dictionary of mapping and meat cooking method
        '''
        meat_list = [r'ground (chicken|turkey|beef|lamb|pork)', 'chicken', 'turkey', 'beef', 'lamb', 'pork', 'fish'] #TODO: potentially add types of shellfish
        output = {}

        meat_directions = {}
        exclude_list = []
        cur_meat = None
        # get directions with meats only
        for direction in directions:
            for meat in meat_list:
                if meat in exclude_list:
                    continue
                if cur_meat != None:
                    for method in methods:
                        if method in direction:
                            output[cur_meat] = method
                else:
                    found_meat = re.search(meat, direction)
                    if found_meat:
                        cur_meat = found_meat[0]
                        meat_directions[found_meat[0]] = direction
                        # prevent duplicates with ground meats
                        to_exclude = found_meat[0].split()[1]
                        exclude_list.append(to_exclude)   
        return output

    def to_cuisine(self, cuisine): 
        pass 