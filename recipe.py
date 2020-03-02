import copy
import re 
from ingredient import *
from nltk.corpus import stopwords

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
    'stiry fry':{
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
        print(recipe_dic['name'])
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
            ingredient = ingredient.to_veg(meats_to_subtitute)

        # make direction veg
        veg_directions = copy.deepcopy(self.directions)
        for i in range(len(veg_directions)):
            direction = veg_directions[i]
            for meat, substitute in meats_to_subtitute.items():
                if meat in direction:
                    veg_directions[i] = direction.replace(meat, substitute)
                    # print(direction)
                if 'meat' in direction:
                    if 'ground meat' in direction:
                        veg_directions[i] = direction.replace('ground_meat', substitute)
                    else:
                        veg_directions[i] = direction.replace('meat', substitute)
                # else:
                #     if 'ground' in meat:
                #         veg_directions[i] = direction.replace(meat.split(' ')[1], substitute)

        # create new recipe object
        veg_recipe = copy.deepcopy(self)
        # veg_recipe.recipe_name = "Vegetarian "+ veg_recipe.recipe_name
        veg_recipe.ingredients = veg_ingredients
        veg_recipe.directions = veg_directions

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
                        # print(found_meat)
                        # to_exclude = found_meat[0].split()[1]
                        # exclude_list.append(to_exclude)   
        return output

    def to_cuisine(self, cuisine):
        for i in self.ingredients:
            print("name:", i.name, "// unit:",i.unit, "// quantity:",i.quantity, "// prep:", i.prep)
        
        return cuisine 
    def get_ingredients_tools_time(self):
        # Steps – parse the directions into a series of steps that each consist of ingredients, tools, methods, and times
        output = []
        for direction in self.directions:
            ingredients = self.get_ingredients(self.ingredients, direction)
            print(direction)
            tools = self.get_tools(self.tools, direction)
            print(self.methods)
            methods = self.get_methods(self.methods, direction)
            time = ""
            output.append([ingredients, tools, methods, time])
        return output

    def get_ingredients(self, ingredients, direction):
        global STOP_WORDS
        ingredients_in_direction = []
        for ingredient in ingredients:
            # tokenize ingredient, remove stop words
            ingredient_set = ingredient.name.split(' ')
            ingredient_set = [w for w in ingredient_set if not w in STOP_WORDS] 
            # get primary words for ingredient name
            ingredient_pos = nltk.pos_tag(ingredient_set)
            ingredient_primary = [w[0] for w in ingredient_pos if w[1] in {'NN', 'NNS'}]

            # tokenize direction, remove stop words
            direction_set = direction.split(' ')
            direction_set = [w for w in direction_set if not w in STOP_WORDS] 

            intersection = set(ingredient_primary).intersection(set(direction_set))
            if len(intersection) > 1:
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
