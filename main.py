from RecipeFetcher import *
from nltk.corpus import wordnet as wn

# initializze recipe fetcher object, can be used to scrap any food
rf = RecipeFetcher()

# grabs meat lasagna recipe 
recipe_json = rf.find_recipe("meat") 
print(recipe_json)

# Parse ingredients for name, quantity, measurement type, descriptor (optional), and preparation (optional)

# Use NLTK library to get a list of ingrdients 
food = wn.synset('ingredient.n.03')
print(wn.synset('ingredient.n.03').definition())
# Hyponyms are more specific cases of a concept/word
print(len(list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))))

# Parsing ingredients using regex 
ingredients = {}
for ingredient in recipe_json["ingredients"]: 
    ingredient["name"], ingredient["quantity"], ingredient["unit"] = parse_ingredient(ingredient)

def parse_ingredient(ingredient): 
    name = ""
    quantity = -1
    unit = ""
    return name, quantity, unit

# Test to cuisine 


# map to relevant classes 




