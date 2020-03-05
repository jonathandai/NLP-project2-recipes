import copy
import re
from ingredient import *
from nltk.corpus import stopwords
import json
import random
import string
from more_itertools import locate
# List of strings
from RecipeFetcher import *

# from RecipeFetcher import *
STOP_WORDS =  set(stopwords.words('english'))
COOKING_METHOD_TO_SUBSTITUTE = { #TODO: add shellfish
    'boil':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'mushroom',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'ribs': 'tempeh',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'bake':{
        'chicken': 'seitan',
        'turkey': 'mushroom',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'mushroom',
        'fish': 'tempeh',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'simmer':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'roast':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'deep fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'deep-fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'stir fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'stir-fry':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'grill':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'steam':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tofu',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    },
    'sautee':{
        'chicken': 'tofu',
        'turkey': 'tofu',
        'beef': 'mushroom',
        'lamb': 'mushroom',
        'pork': 'jackfruit',
        'fish': 'tofu',
        'ground': 'beans',
        'ham': 'tempeh',
        'liver': 'tofu',
        'bacon': 'vegetarian bacon',
        'sausage': 'tofu',
        'veal': 'seitan',
        'carp': 'lentils',
        'catfish': 'lentils',
        'salmon': 'lentils',
        'tilapia': 'lentils',
        'tuna': 'lentils',
        'trout': 'lentils',
        'crayfish': 'lentils',
        'lobster': 'lentils',
        'shrimp': 'lentils',
        'prawns': 'lentils',
        'oyster': 'lentils',
        'mussel': 'lentils' ,
        'clams': 'lentils'
    }
}
TIME_WORDS = ['minute', 'minutes', 'min', 'mins', 'second', 'seconds', 's', 'hour', 'hours', 'hr', 'hrs', 'h']

class Recipe(object):

    def __init__(self, recipe_dic):
        self.recipe_dic = recipe_dic
        self.recipe_name = recipe_dic["name"]
        # list of ingredients objects
        ingredients_list = recipe_dic['ingredients']
        ingredient_objects = []
        for ing in ingredients_list:
            ingredient_objects.append(Ingredient(ing))
        self.ingredients = ingredient_objects
        # directions object
        self.directions = recipe_dic['directions']
        # set tools
        self.tools = recipe_dic['tools']
        # set methods
        self.methods = recipe_dic['methods']
        # set url
        self.url = recipe_dic["top_url"]

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

    def print_recipe(self):
        print("Recipe Name:", self.recipe_name[0])
        print("Recipe URL:", self.url, "\n")
        print("Ingredients:")
        for ing in self.ingredients:
            print(ing)

        print("\n")
        print("Directions:")

        direction_items = self.get_ingredients_tools_methods_times()
        # print(direction_items, '-------------------------')
        i = 1
        for dir in self.directions:
            print("Step", i, ":" , dir)
            # print(i, '------------------')
            # print(direction_items)
            curr_direction_item = direction_items[i-1]

            print("Ingredients:", curr_direction_item[0])
            print("Tools:", curr_direction_item[1])
            print("Methods:", curr_direction_item[2])
            print("Additional methods:", curr_direction_item[3])
            print("Times:", curr_direction_item[4])
            i += 1
            print('-----------------------------------')
        print("\n")

        print("Tools needed:", self.tools)
        print("Methods required:", self.methods)
        print("Primary cooking method:", self.get_primary_cooking_method())
        print("\n")
        print("---------------------------------------------------------------------------------")


    def get_primary_cooking_method(self):
        direction_items = self.get_ingredients_tools_methods_times()
        index = 1
        curr_direction_item = direction_items[index-1]
        times = curr_direction_item[3]
        methods = self.methods
        biggest_time = "0"
        primary_method = ''
        if len(self.methods) > 1:
            for method in self.methods:
                for time in times:
                    if time >= biggest_time:
                        biggest_time = time
                        primary_method = method
        else:
            primary_method = self.methods

        return primary_method


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

        unhealthy_recipe = copy.deepcopy(self)

        # create new recipe object
        unhealthy_recipe.ingredients = unhealthy_ingredients
        unhealthy_recipe.directions = unhealthy_directions

        return unhealthy_recipe

    def to_veg(self):
        # returns a copy of vegetarian version of recipe
        # get mapping of meat to substitute
        methods = ['boil', 'bake','simmer','roast','fry','deep fry','deep-fry','stiry fry','stir-fry','grill','steam','sautee']
        meats_to_cooking_method = self.map_meat_to_cooking_method(self.directions, methods)
        meats_to_subtitute = self.meat_to_substitute(meats_to_cooking_method)
        # print(meats_to_subtitute)
        # make ingredients veg
        veg_ingredients = copy.deepcopy(self.ingredients)
        for ingredient in veg_ingredients:
            ingredient = ingredient.to_veg(meats_to_subtitute)
        # print(veg_ingredients, '-----------------------------------')
        # make direction veg
        veg_directions = []
        for i in range(len(self.directions)):
            new_direction = self.directions[i]
            for meat, substitute in meats_to_subtitute.items():
                if meat in new_direction:
                    new_direction = new_direction.replace(meat, substitute)
                if 'meat' in new_direction:
                    if 'ground meat' in new_direction:
                        new_direction = new_direction.replace('ground meat', substitute)
                    else:
                        new_direction = new_direction.replace('meat', substitute)
                # else:
                #     if 'ground' in meat:
                #         veg_directions[i] = direction.replace(meat.split(' ')[1], substitute)
            veg_directions.append(new_direction)
        # create new recipe object
        veg_recipe = copy.deepcopy(self)
        # veg_recipe.recipe_name = "Vegetarian "+ veg_recipe.recipe_name
        veg_recipe.ingredients = veg_ingredients
        veg_recipe.directions = veg_directions
        # print(veg_recipe.directions)

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
        meat_list = ['ground chicken', 'ground beef', 'ground turkey', 'ground pork', 'ground lamb','ground fish', 'chicken', 'turkey', 'beef', 'lamb', 'pork', 'fish'] #TODO: potentially add types of shellfish
        output = {}

        exclude_list = []
        # get directions with meats only
        for direction in directions:
            for meat in meat_list:
                if meat in exclude_list:
                    continue
                if meat in direction:
                    for method in methods:
                        if method in direction:
                            output[meat] = method
                    if 'ground' in meat:
                        meat_tokens = meat.split(' ')
                        exclude_list.append(meat_tokens[1])
        # print('checking ignredients')
        # jank case for if meat not found in directions
        for ingredient in self.ingredients:
            for meat in meat_list:
                if meat in exclude_list:
                    continue
                if meat in ingredient.name:
                    output[meat] = 'stir fry'
                    if 'ground' in meat:
                        meat_tokens = meat.split(' ')
                        exclude_list.append(meat_tokens[1])

        return output


    def get_ingredients_tools_methods_times(self):
        # Steps – parse the directions into a series of steps that each consist of ingredients, tools, methods, and times
        output = []
        for direction in self.directions:
            ingredients = self.get_ingredients(self.ingredients, direction)
            tools = self.get_tools(self.tools, direction)
            methods = self.get_methods(self.methods, direction)
            times = self.get_times(direction)
            other_methods = self.get_other_methods(direction)
            output.append([ingredients, tools, methods, other_methods, times])

        return output

    def get_other_methods(self, direction):
        OTHER_COOKING_METHODS = ["chop", "grate", "stir", "shake", "mince", "crush", "squeeze", "julienne", "slice", "baste", "fillet", "garnish"]
        methods_in_direction = []
        for method in OTHER_COOKING_METHODS:
            if method in direction:
                methods_in_direction.append(method)
        return methods_in_direction

    def get_ingredients(self, ingredients, direction):
        global STOP_WORDS
        ingredients_in_direction = []
        for ingredient in ingredients:
            # tokenize ingredient, remove stop words
            ingredient_set = ingredient.name.split(' ')
            ingredient_set = [w for w in ingredient_set if not w in STOP_WORDS]
            ingredient_set = [w for w in ingredient_set if w != ""]
            # get primary words for ingredient name
            ingredient_pos = nltk.pos_tag(ingredient_set)
            ingredient_primary = [w[0] for w in ingredient_pos if w[1] in {'NN', 'NNS'}]

            # tokenize direction, remove stop words
            direction_set = direction.split(' ')
            direction_set = [w for w in direction_set if not w in STOP_WORDS]
            intersection = set(ingredient_primary).intersection(set(direction_set))
            if len(intersection) >= 1:
                ingredients_in_direction.append(ingredient.name)
        return ingredients_in_direction

    def get_tools(self, tools, direction):
        tools_in_direction = []
        for tool in tools:
            if tool in direction:
                tools_in_direction.append(tool)
            else:
                # get word to tools matchings
                do = 'something'
        return tools_in_direction

    def get_methods(self, methods, direction):
        methods_in_direction = []
        for method in methods:
            if method in direction:
                methods_in_direction.append(method)
        return methods_in_direction

    def get_times(self, direction):
        times = []
        global TIME_WORDS
        direction = direction.translate(str.maketrans('', '', string.punctuation))
        direction_tokens = direction.split(' ')
        # print(direction)
        for time_word in TIME_WORDS:
            if time_word in direction_tokens:
                index_pos_list= list(locate(direction_tokens, lambda a: a == time_word))
                for time_index in index_pos_list:
                    flag = True
                    while time_index >= 0 and flag:
                        element = direction_tokens[time_index]
                        if element.isdigit():
                            element = float(element)
                            times.append(str(element) + ' ' + time_word)
                            flag = False
                        else:
                            time_index = time_index - 1

        return times




    def in_food_group(self, ingredient):

        '''
        Checks if a string (ingredient) is in one of the ingredient text files
        '''
        for fg in self.food_groups:
            if any(word in ingredient for word in self.food_groups[fg]):
                return fg
        return False

    def to_asian_cuisine(self, cuisine):
        chinese_cuisine = {
            "spice": ["garlic", "ginger", "clove", "star anise", "peppercorn", "cumin", "sesame seed", "five spice", "sichuan", "white pepper", "bay leaf"],
            "sauce": ["soy sauce", "oyster sauce", "rice vinegar", "seasame oil"],
            "vegetable": ["bitter melon", "chinese cabbage", "bok choy", "eggplant", "shiitake mushroom"],
            "carb": ["white rice", "egg noodles"],
            "tool": ["wok"],
            "method": ["stir-fry"],
            "restriction": ["milk", "cheese", "cream"]
        }

        thai_cuisine = {
            "spice": ["garlic", "tumeric", "ginger", "basil", "lemongrass", "galangal", "shallots","red chilis"],
            "sauce": ["fish sauce", "thai curry", "peanut sauce", "dried thai chili dipping sauce"],
            "carb": ["sticky rice", "pad-thai noodles", "pad-see-ew noodles"],
            "tool": ["wok"],
            "method": ["stir-fry"],
            "restriction": ["milk", "cheese", "cream"]
        }

        korean_cuisine = {
            "spice": ["kimchi", "garlic", "ginger", "scallions", "kochukaru chili flakes", "perilla"],
            "sauce": ["sesame oil", "gochujang", "soy sauce", "ssamjang", "ganjang"],
            "carb": ["short-grain rice", "naengmyon"],
            "tool": ["wok"],
            "method": ["stir-fry"],
            "restriction": ["milk", "cream"]
        }

        cuisine_map = {
            "chinese": chinese_cuisine,
            "thai": thai_cuisine,
            "korean": korean_cuisine
        }

        if cuisine in cuisine_map.keys():
            sub = cuisine_map[cuisine]
        else:
            print('Sorry, this cuisine transformation is not supported.')
            return

        universal_ingredients = ['salt', 'pepper', 'black pepper']

        # for i in self.ingredients:
        #     print("name:", i.name, "// unit:", i.unit, "// quantity:", i.quantity, "// prep:", i.prep)
        # print('----------------------------------------')
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
        ch_json["name"] = [self.recipe_name[0] + " (" + cuisine.capitalize() + " Style)"]

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
                    ing = random.choice(sub[ing_category])
                    sub[ing_category].remove(ing)
                    if ing_category in ["spice", "sauce"]:
                        ing += " (to taste)"

                    rep = Ingredient(replaced_ing)
                    new_dir = []
                    for direction in ch_json["directions"]:
                        curr = direction.replace(rep.name, ing)
                        new_dir.append(curr)
                    ch_json["directions"] = new_dir
            if not any(word in ing for word in sub["restriction"]):
                new_ing.append(ing)
        ch_json["ingredients"] = new_ing
        ch_json["nutrition"].append("* Disclaimer: nutrition facts may differ post recipe transformation *")

        trans_recipe = Recipe(ch_json)
        return trans_recipe
