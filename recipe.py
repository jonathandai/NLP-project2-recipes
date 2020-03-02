import copy
import re
from ingredient import *

from RecipeFetcher import *
# COOKING_METHOD_TO_SUBSTITUTE = { #TODO: add shellfish
# """
# 'liver': 'tofu',
#
#     'quail': 'eggplant',
#     'rabbit': 'beans',
#     'pheasant': 'eggplant',
#     'goose': 'eggplant',
#
#
# """
#     'boil':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'mushroom',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'ribs': 'tempeh',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils',
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils',
#         'clams': 'lentils'
#     },
#     'bake':{
#         'chicken': 'seitan',
#         'turkey': 'mushroom',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'mushroom',
#         'fish': 'tempeh',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils',
#         'clams': 'lentils'
#     },
#     'simmer':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'roast':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'fry':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'deep fry':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'deep-fry':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'stiry fry':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'stir-fry':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'grill':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'steam':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tofu',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     },
#     'sautee':{
#         'chicken': 'tofu',
#         'turkey': 'tofu',
#         'beef': 'mushroom',
#         'lamb': 'mushroom',
#         'pork': 'jackfruit',
#         'fish': 'tofu',
#         'ground': 'beans',
#         'ham': 'tempeh',
#         'liver': 'tofu',
#         'bacon': 'vegetarian bacon',
#         'sausage': 'tofu',
#         'veal': 'seitan',
#         'carp': 'lentils',
#         'catfish': 'lentils',
#         'salmon': 'lentils',
#         'tilapia': 'lentils',
#         'tuna': 'lentils'
#         'trout': 'lentils',
#         'crayfish': 'lentils',
#         'lobster': 'lentils',
#         'shrimp': 'lentils',
#         'prawns': 'lentils',
#         'oyster': 'lentils',
#         'mussel': 'lentils' ,
#         'clams': 'lentils'
#     }
# }
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
        # set tools


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
        healthy_directions = copy.deepcopy(self.directions)

        for i in range(len(healthy_directions)):
            curr_direction = healthy_directions[i]
            #print(curr_direction)
            for unhealthy_ing in healthy_substitutes:
                if unhealthy_ing in curr_direction:
                    curr_direction = curr_direction.replace(unhealthy_ing, healthy_substitutes[unhealthy_ing])
                    healthy_directions[i] = curr_direction
                    #print(unhealthy_ing)
                    #print(healthy_substitutes[unhealthy_ing])

        healthy_recipe = copy.deepcopy(self)

        # create new recipe object
        healthy_recipe.ingredients = healthy_ingredients
        healthy_recipe.directions = healthy_directions

        return healthy_recipe

    def from_healthy(self):
        #returns copy of unhealthy versio of recipe

        unhealthy_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in unhealthy_ingredients:
            ingredient = ingredient.from_healthy()

        unhealthy_directions = copy.deepcopy(self.directions)

        for i in range(len(unhealthy_directions)):
            curr_direction = unhealthy_directions[i]
            #print(curr_direction)
            for healthy_ing in unhealthy_substitutes:
                if healthy_ing in curr_direction:
                    curr_direction = curr_direction.replace(healthy_ing, unhealthy_substitutes[healthy_ing])
                    unhealthy_directions[i] = curr_direction
                    #print(curr_direction)
                # elif "bake" in curr_direction:
                #     curr_direction = curr_direction.replace("bake", "fry")
                #     unhealthy_directions[i] = curr_direction

        unhealthy_recipe = copy.deepcopy(self)

        # create new recipe object
        unhealthy_recipe.ingredients = unhealthy_ingredients
        unhealthy_recipe.directions = unhealthy_directions

        return unhealthy_recipe

    def to_veg(self):
    #     # returns a copy of vegetarian version of recipe

    #     # make ingredients healthy
    #     veg_ingredients = copy.deepcopy(self.ingredients)
    #     for ingredient in veg_ingredients:
    #         ingredient = ingredient.to_veg()


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
                        # print(found_meat)
                        # to_exclude = found_meat[0].split()[1]
                        # exclude_list.append(to_exclude)
        return output
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

            print("name:", i.name, "// unit:",i.unit, "// quantity:",i.quantity, "// prep:", i.prep)

        return cuisine

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

    def get_ingredients_tools_time(self):
        pass
