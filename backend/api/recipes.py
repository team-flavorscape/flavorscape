from model.recipe import Recipe
from model.allergen import Allergen
from model.dislike import Dislike

from api.dislikes import dislikes

IMG_BASE_URL_LARGE='https://img.hellofresh.com/w_1000,q_auto,f_auto,c_limit,fl_lossy/hellofresh_s3'

class Recipes:
    def __init__(self, json_dict):
        self.recipes = json_dict

        allergens = list({a['name'] for r in self.recipes for a in r['allergens']})
        self.allergens = []
        for i in range(len(allergens)):
            self.allergens.append(Allergen(id=i, name=allergens[i]))

    def count(self):
        return len(self.recipes)

    def get_recipe(self, id):
        r = self.recipes[id]
        ingredients = [i['name'] for i in r['ingredients']]
        allergens = [a['name'] for a in r['allergens']]
        return Recipe(
                id=id,
                name=r['name'],
                img_url=IMG_BASE_URL_LARGE + r['imagePath'],
                ingredients=ingredients,
                allergens=allergens,
            )

    def get_recipe_by_name(self, name):
        for i,r in enumerate(self.recipes):
            if r['name'].lower() == name.lower():
                return self.get_recipe(i)

    def get_allergens(self):
        return self.allergens

    def get_allergen_name(self, id):
        return self.allergens[id].name

    def get_dislikes(self):
        return [Dislike(id=i, name=d.name) for i,d in enumerate(dislikes)]

    def get_dislike_name(self, id):
        return dislikes[id].name
