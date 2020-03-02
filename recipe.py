import copy
import re 
from ingredient import *
from directions import *
# from RecipeFetcher import *
class Recipe(object):

    def __init__(self, recipe_dic):
        self.recipe_name = recipe_dic["name"]
        # list of ingredients objects
        ingredients_list = recipe_dic['ingredients']
        ingredient_objects = []
        for ing in ingredients_list:
            ingredient_objects.append(Ingredient(ing))
        # print(ingredient_objects[1].name)
        # print(ingredient_objects[1].unit)
        # print(ingredient_objects[1].quantity)
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

        # make ingredients healthy
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg()
        

        # create new recipe object
        veg_recipe = Recipe(self.directions)

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
        # chinese_subsitutions = {"carb": ["rice", "egg noodle"], "protein": [], "sauce": ["soy sauce"], "restrictions":[]}

        # figure out best guess for cuisine 
        # if not same
            # transform to XX cuisine 
            # 


        for i in self.ingredients:
            print("name:", i.name, "// unit:", i.unit, "// quantity:", i.quantity, "// prep:", i.prep)

        components = {}
        # identify main components of dish (carb, protein, seasoning, dairy)
        components["carb"] = ""


        return cuisine 
