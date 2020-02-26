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
