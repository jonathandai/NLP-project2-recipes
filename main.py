from RecipeFetcher import *
from recipe import *
from nltk.corpus import wordnet as wn

# initialize recipe fetcher object, can be used to scrap any food
rf = RecipeFetcher()

# grabs meat lasagna recipe 
# recipe_json = rf.find_recipe("meat")

# RF = RecipeFetcher()
# recipe = RF.find_recipe('chicken alfredo')
recipe_json = rf.find_recipe('meat')
recipe = Recipe(recipe_json)
print(recipe_json)
# print(recipe.ingredients)
# print(recipe.directions)
# veg_recipe = recipe.to_veg()
# print(veg_recipe.directions)
# print(recipe_json)

# Parse ingredients for name, quantity, measurement type, descriptor (optional), and preparation (optional)

# Use NLTK library to get a list of ingrdients 
# food = wn.synset('ingredient.n.03')
# print(wn.synset('ingredient.n.03').definition())
# Hyponyms are more specific cases of a concept/word
# print(len(list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))))

# Parsing ingredients using regex 
# ingredients = {}
# for ingredient in recipe_json["ingredients"]: 
#     ingredient["name"], ingredient["quantity"], ingredient["unit"] = parse_ingredient(ingredient)

# def parse_ingredient(ingredient): 
#     name = ""
#     quantity = -1
#     unit = ""
#     return name, quantity, unit

# Test to cuisine 
test_recipe = Recipe(recipe_json)
test_recipe.to_asian_cuisine("thai")
print(test_recipe)

# map to relevant classes 




