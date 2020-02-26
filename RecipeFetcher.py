from bs4 import BeautifulSoup
import requests
import re

from recipe import Recipe


class RecipeFetcher:

   def __init__(self):
      # nothing needed yet?
      print()

   def search_recipes(self, keywords): 
        search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
        search_url = search_base_url %(keywords.replace(' ','+'))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content)
        return [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]

   def scrape_recipe(self, food_name, recipe_url, to_recipe_object=False):
      page_html = requests.get(recipe_url)
      page_graph = BeautifulSoup(page_html.content)
      
      ingredients = [ingredient.text for ingredient in\
                                 page_graph.find_all('span', {'itemprop':'recipeIngredient'})]
      
      directions = [direction.text.strip() for direction in\
                                 page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                 if direction.text.strip()]
      tools = self.scrape_nutrition_facts(recipe_url)

      methods = self.find_cooking_methods(directions)
      
      primary_cooking_methods = self.map_meat_to_cooking_method(directions, methods)
      
      results = None
      if to_recipe_object:
         results = Recipe(food_name, ingredients=ingredients, directions=directions, methods=methods, primary_cooking_method=primary_cooking_methods)
      else:
         results = {}

         results['ingredients'] = ingredients

         results['directions'] = directions

         results['tools'] = tools

         results['methods'] = methods

         results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

      return results

   def find_tools(self, steps):
      tool_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'
      directions = " ".join(steps)
      cooking_tools = re.findall(tool_regex, directions)
      return set(cooking_tools)

   def find_cooking_methods(self, steps):
      method_regex = '(boil|bake|simmer|roast|fry|deep fry|deep-fry|stiry fry|stir-fry|grill|steam|sautee)'
      directions = " ".join(steps)
      cooking_methods = re.findall(method_regex, directions)
      return set(cooking_methods)

   def map_meat_to_cooking_method(self, directions, methods):
      '''
      returns dictionary of mapping and meat cooking method
      '''
      meat_list = [r'ground (chicken|turkey|beef|lamb|pork)', 'chicken', 'turkey', 'beef', 'lamb', 'pork', 'fish'] #TODO: potentially add types of shellfish
      output = {}
      
      meat_directions = {}
      exclude_list = []
      cur_meat = None
      cur_method = None
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
      # print('directions with meat')
      # print(meat_directions) 
      # print(output)      
      return output

   def scrape_nutrition_facts(self, recipe_url):
      results = []

      nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)
      page_html = requests.get(nutrition_facts_url)
      page_graph = BeautifulSoup(page_html.content, 'html.parser')

      r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")
      # finds all rows with class="nutrition-row" 
      for nutrient_row in page_graph.find_all(class_='nutrition-row'):
          nutrient = {}
          # separates into array of all the 'span' tags 
          span_elements = nutrient_row.find_all('span')
          # splits the first tag to ingredient name and ingredient quantity 
          ingredient_data = span_elements[0].text.split(': ')
          ingredient_name = ingredient_data[0]
          ingredient_amount = ingredient_data[1]
          # splits ingredient amount by amount and unit 
          ingredient_amount_split = r.match(ingredient_amount).groups()

          # add the results of nutrients to the list 
          nutrient['name'] = ingredient_name
          nutrient['amount'] = ingredient_amount_split[0]
          nutrient['unit'] = ingredient_amount_split[1]
          # only looks for daily value if there is a 4th entry, kinda jank wanted to search by class="daily-value" but wasn't working
          if len(span_elements) == 4:
            nutrient['daily_value'] = span_elements[3].text
          results.append(nutrient)

      return results

   def find_recipe(self, food_name): 
      food_search = self.search_recipes(food_name)[0]
      recipe = self.scrape_recipe(food_name, food_search)
      # print(recipe)
      return recipe

# testing to_veg
print('fuck')
RF = RecipeFetcher()
meat_lasagna = RF.find_recipe('meat lasagna')


# encode to classes

"""
Returns'

{
   "ingredients":[
      "12 whole wheat lasagna noodles",
      "1 pound lean ground beef",
      "2 cloves garlic, chopped",
      "1/2 teaspoon garlic powder",
      "1 teaspoon dried oregano, or to taste",
      "salt and ground black pepper to taste",
      "1 (16 ounce) package cottage cheese",
      "2 eggs",
      "1/2 cup shredded Parmesan cheese",
      "1 1/2 (25 ounce) jars tomato-basil pasta sauce",
      "2 cups shredded mozzarella cheese"
   ],
   "directions":[
      "Preheat oven to 350 degrees F (175 degrees C).",
      "Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the lasagna noodles a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.",
      "Place the ground beef into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.",
      "In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.",
      "Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.",
      "Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving."
   ],
   "nutrition":[
      {
         "name":"Total Fat",
         "amount":"19.3",
         "unit":"g",
         "daily_value":"30 %"
      },
      {
         "name":"Saturated Fat",
         "amount":"9.0",
         "unit":"g"
      },
      {
         "name":"Cholesterol",
         "amount":"115",
         "unit":"mg",
         "daily_value":"38 %"
      },
      {
         "name":"Sodium",
         "amount":"999",
         "unit":"mg",
         "daily_value":"40 %"
      },
      {
         "name":"Potassium",
         "amount":"717",
         "unit":"mg",
         "daily_value":"20 %"
      },
      {
         "name":"Total Carbohydrates",
         "amount":"47.1",
         "unit":"g",
         "daily_value":"15 %"
      },
      {
         "name":"Dietary Fiber",
         "amount":"6.3",
         "unit":"g",
         "daily_value":"25 %"
      },
      {
         "name":"Protein",
         "amount":"35.6",
         "unit":"g",
         "daily_value":"71 %"
      },
      {
         "name":"Sugars",
         "amount":"12",
         "unit":"g"
      },
      {
         "name":"Vitamin A",
         "amount":"855",
         "unit":"IU"
      },
      {
         "name":"Vitamin C",
         "amount":"2",
         "unit":"mg"
      },
      {
         "name":"Calcium",
         "amount":"361",
         "unit":"mg"
      },
      {
         "name":"Iron",
         "amount":"4",
         "unit":"mg"
      },
      {
         "name":"Thiamin",
         "amount":"0",
         "unit":"mg"
      },
      {
         "name":"Niacin",
         "amount":"11",
         "unit":"mg"
      },
      {
         "name":"Vitamin B6",
         "amount":"0",
         "unit":"mg"
      },
      {
         "name":"Magnesium",
         "amount":"74",
         "unit":"mg"
      },
      {
         "name":"Folate",
         "amount":"41",
         "unit":"mcg"
      }
   ]
}
"""