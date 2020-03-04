from RecipeFetcher import *
from recipe import *
from nltk.corpus import wordnet as wn

def main(): 
    # initialize recipe fetcher object, can be used to scrap any food
    rf = RecipeFetcher()

    # prompt user for what recipe they want to find 
    food_name = input("Please enter what recipe you want to search for:\n")

    # fetch the allrecipes page
    # try: 
    recipe_json = rf.find_recipe(food_name)
    recipe = Recipe(recipe_json)
    # print initial recipe
    print("Here is the top result for your search: \n")
    recipe.print_recipe()

    # ask user what transformation they want to perform
    transformation = input("Please enter the transformation you want (vegetarian, healthy, asian). If none, enter any character:\n")
    if transformation == "vegetarian":
        veg = recipe.to_veg()
        veg.print_recipe()
    elif transformation == "healthy":
        healthy = recipe.to_healthy()
        healthy.print_recipe()
    elif transformation == "asian": 
        cuisine = input("Please input which asian region you want to transform your recipe to (current supported options include: chinese, korean, and thai):\n")
        while cuisine not in ["chinese", "korean", "thai"]:
            cuisine = input("Please input a supported option (chinese, korean, and thai):\n")
        asian = recipe.to_asian_cuisine(cuisine)
        asian.print_recipe()
    else: 
        print("Happy cooking!")
    # except: 
    #     print("Invalid input, please try again.")
    #     main() 

if __name__ == "__main__":
    main() 
