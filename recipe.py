import copy
import re 
from ingredient import *
import json
import random 
# from RecipeFetcher import *
class Recipe(object):

    def __init__(self, recipe_dic):
        self.recipe_dic = recipe_dic
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


        fruits = set([line.strip() for line in open('./ingredient_data/fruits.txt')])
        spices = set([line.strip() for line in open('./ingredient_data/spices.txt')])
        vegetables = set([line.strip() for line in open('./ingredient_data/vegetables.txt')])
        sauces = set([line.strip() for line in open('./ingredient_data/sauces.txt')])
        carbs = set([line.strip() for line in open('./ingredient_data/carbs.txt')])
        binders = set([line.strip() for line in open('./ingredient_data/binders.txt')])

        self.food_groups = {
            "fruit": fruits,
            "spice": spices,
            "vegetable": vegetables,
            "sauce": sauces,
            "carb": carbs,
            "binder": binders,
        }

        
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
    #     # returns a copy of vegetarian version of recipe

    #     # make ingredients healthy
    #     veg_ingredients = copy.deepcopy(self.ingredients)
    #     for ingredient in veg_ingredients:
    #         ingredient = ingredient.to_veg()
        

    #     # create new recipe object
    #         veg_recipe = Recipe(self.directions)

    #     return veg_recipe
        
    # def map_meat_to_cooking_method(self, directions, methods):
    #     '''
    #     returns dictionary of mapping and meat cooking method
    #     '''
    #     meat_list = [r'ground (chicken|turkey|beef|lamb|pork)', 'chicken', 'turkey', 'beef', 'lamb', 'pork', 'fish'] #TODO: potentially add types of shellfish
    #     output = {}

    #     meat_directions = {}
    #     exclude_list = []
    #     cur_meat = None
    #     # get directions with meats only
    #     for direction in directions:
    #         for meat in meat_list:
    #             if meat in exclude_list:
    #                 continue
    #             if cur_meat != None:
    #                 for method in methods:
    #                     if method in direction:
    #                         output[cur_meat] = method
    #             else:
    #                 found_meat = re.search(meat, direction)
    #                 if found_meat:
    #                     cur_meat = found_meat[0]
    #                     meat_directions[found_meat[0]] = direction
    #                     # prevent duplicates with ground meats
    #                     to_exclude = found_meat[0].split()[1]
    #                     exclude_list.append(to_exclude)   
    #     return output
        pass


    # def find_and_replace(self, item, subsitute):
    #     meat_directions = {}
    #     exclude_list = []
    #     cur_meat = None
    #     # get directions with meats only
    #     for direction in directions:
    #         for meat in meat_list:
    #             if meat in exclude_list:
    #                 continue
    #             if cur_meat != None:
    #                 for method in methods:
    #                     if method in direction:
    #                         output[cur_meat] = method
    #             else:
    #                 found_meat = re.search(meat, direction)
    #                 if found_meat:
    #                     cur_meat = found_meat[0]
    #                     meat_directions[found_meat[0]] = direction
    #                     # prevent duplicates with ground meats
    #                     to_exclude = found_meat[0].split()[1]
    #                     exclude_list.append(to_exclude)   
    

    def in_food_group(self, ingredient):
        
        '''
        Checks if a string (ingredient) is in one of the ingredient text files
        '''
        for fg in self.food_groups:
            if any(word in ingredient for word in self.food_groups[fg]):
                return fg
        return False
        
    def to_chinese(self):
        chinese_cuisine = {
            "spice": ["garlic", "ginger", "clove", "star anise", "peppercorn", "cumin", "sesame seed", "five spice", "sichuan", "white pepper", "bay leaf"],
            "sauce": ["soy sauce", "oyster sauce", "rice vinegar", "seasame oil"],
            "vegetable": ["bitter melon", "chinese cabbage", "bok choy", "eggplant", "shiitake mushroom"],
            "carb": ["white rice", "egg noodles"],
            "tool": ["wok"],
            "method": ["stir-fry"],
            "restriction": ["milk", "cheese", "cream"]
        }

        universal_ingredients = ['salt'] 

        for i in self.ingredients:
            print("name:", i.name, "// unit:", i.unit, "// quantity:", i.quantity, "// prep:", i.prep)
        print('----------------------------------------')
        ingredient_split = {
            "fruit": [],
            "spice": [],
            "vegetable": [],
            "sauce": [],
            "carb": [],
            "binder": [],
        }

        # chinese version of recipe json 
        ch_json = self.recipe_dic.copy() 
        ch_json["name"] = self.recipe_name[0] + " (Chinese Style)" 

        for ingredient in self.ingredients:
            food_type = self.in_food_group(ingredient.name)
            if food_type:
                ingredient_split[food_type].append(ingredient)
                continue

        new_ing = []
        new_dir = []
        for ing in ch_json["ingredients"]: 
            # first remove restrictions 
            ing_category = self.in_food_group(ing)
            if ing_category:
                if ing_category in ["carb", "spice", "sauce"] and ing not in universal_ingredients:
                    replaced_ing = ing
                    ing = random.choice(chinese_cuisine[ing_category])
                    chinese_cuisine[ing_category].remove(ing)
                    if ing_category in ["spice", "sauce"]: 
                        ing += " (to taste)"

                    rep = Ingredient(replaced_ing)
                    new_dir = []
                    for direction in ch_json["directions"]:
                        curr = direction.replace(rep.name, ing)
                        new_dir.append(curr)
                    ch_json["directions"] = new_dir
            if not any(word in ing for word in chinese_cuisine["restriction"]):
                new_ing.append(ing)
        ch_json["ingredients"] = new_ing
        ch_json["nutrition"].append("* Disclaimer: nutrition facts may differ post recipe transformation *")
        
        print(ch_json)
        trans_recipe = Recipe(ch_json)
        return trans_recipe
