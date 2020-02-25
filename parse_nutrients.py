from bs4 import BeautifulSoup

import requests

import re


class RecipeFetcher:

    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'

    def search_recipes(self, keywords): 
        search_url = self.search_base_url %(keywords.replace(' ','+'))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content)

        return [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]

    def scrape_recipe(self, recipe_url):
      results = {}

      # regex for finding necessary tools
      tool_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'

      page_html = requests.get(recipe_url)
      page_graph = BeautifulSoup(page_html.content)

      results['ingredients'] = [ingredient.text for ingredient in\
                                page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

      results['directions'] = [direction.text.strip() for direction in\
                                page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                if direction.text.strip()]

      results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

      # results['tools'] = self.find_tools(results['directions'])

      return results

    # def find_tools(self, instruction_words):
    #   """
    #   looks for any and all cooking tools apparent in the instruction text by using the tool_indicator_regex
    #   variable
    #   """
    #   tool_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'
    #   cooking_tools = []
    #   for step in instruction_words:
    #     for word in step:
    #       if re.search(tool_regex, word, flags=re.I):
    #         cooking_tools.append(word)
    #     wordset = set(cooking_tools)
    #   return wordset

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

rf = RecipeFetcher()
meat_lasagna = rf.search_recipes('meat lasagna')[0]
recipe = rf.scrape_recipe(meat_lasagna)
print(recipe)


# encode to classes
# find tools

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