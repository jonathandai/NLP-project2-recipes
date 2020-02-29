import copy
import re 
from Ingredient import *
from directions import *
# from RecipeFetcher import *
COOKING_METHOD_TO_SUBSTITUTE = { #TODO: add shellfish
    'boil':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'mushroom',
        'fish': 'tofu',
        'ground': 'beans'
    }, 
    'bake':{
        'chicken': 'seitan',
        'turkey': 'mushroom',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'mushroom',
        'fish': 'tempeh',
        'ground': 'beans'
    },
    'simmer':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'roast':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'deep fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'deep-fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'stiry fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'stir-fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'grill':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'steam':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    },
    'sautee':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans'
    }
}
class Recipe(object):

    def __init__(self, recipe_dic):
        self.recipe_name = recipe_dic["name"]
        # list of ingredients objects
        ingredients_list = recipe_dic['ingredients']
        ingredient_objects = []
        for ing in ingredients_list:
            ingredient_objects.append(Ingredient(ing))
        self.ingredients = ingredient_objects
        # directions object
        self.directions = recipe_dic['directions']
        
    def to_healthy(self):
        # returns a copy of healthy version of recipe

        # make ingredients healthy
        healthy_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in healthy_ingredients:
            ingredient = ingredient.to_healthy()
        
        # make directions healthy
        healthy_directions = self.directions.to_healthy()

        # create new recipe object
        healthy_recipe = Recipe(healthy_directions)

        return healthy_recipe
        

    def to_veg(self):
        # returns a copy of vegetarian version of recipe
        # get mapping of meat to substitute
        methods = ['boil', 'bake','simmer','roast','fry','deep fry','deep-fry','stiry fry','stir-fry','grill','steam','sautee']
        meats_to_cooking_method = self.map_meat_to_cooking_method(self.directions, methods)
        meats_to_subtitute = self.meat_to_substitute(meats_to_cooking_method)

        # make ingredients veg
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg()
        
        # create new recipe object
        # veg_recipe = Recipe(veg_ingredients, self.directions)
        veg_recipe = None

        return veg_recipe
    
    def meat_to_substitute(self, meat_to_cooking_method):
        global COOKING_METHOD_TO_SUBSTITUTE
        output = {}
        for meat, method in meat_to_cooking_method.items():
            if meat.split(' ')[0] != 'ground':
                output[meat] = COOKING_METHOD_TO_SUBSTITUTE[method][meat]
            else:
                output[meat] = COOKING_METHOD_TO_SUBSTITUTE[method]['ground']
        return output

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
        return cuisine 
