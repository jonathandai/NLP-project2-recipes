from RecipeFetcher import *

# initializze recipe fetcher object, can be used to scrap any food
rf = RecipeFetcher()

# grabs meat lasagna recipe 
recipe_json = rf.find_recipe("meat lasagna") 

# map to relevant classes 


