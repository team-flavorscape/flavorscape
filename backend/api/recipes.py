from model.recipe import Recipe
from model.allergen import Allergen
from model.dislike import Dislike

from api.dislikes import dislikes

IMG_BASE_URL_LARGE='https://img.hellofresh.com/w_1000,q_auto,f_auto,c_limit,fl_lossy/hellofresh_s3'

class Recipes:
    def __init__(self, json_dict):
        self.recipes = json_dict

        self.recipe_index = {} # dict to speed up access by name
        for i,r in enumerate(self.recipes):
            self.recipe_index[r['name']] = i

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
        return self.get_recipe(self.recipe_index[name])

    def get_allergens(self):
        return self.allergens

    def get_allergen(self, id):
        return self.allergens[id]

    def get_allergen_name(self, id):
        return self.allergens[id].name

    def get_dislikes(self):
        return [Dislike(id=i, name=d.name) for i,d in enumerate(dislikes)]

    def get_dislike(self, id):
        return dislikes[id]

    def get_dislike_name(self, id):
        return dislikes[id].name

    def get_dislike_ingredients_by_name(self, name):
        out = []
        for d in dislikes:
            if d.name == name:
                out = d.ingredients
                break

        return out

    def filter_allergens(self, recipe_ids: list[int], allergens: list[str]) -> list[int]:
        '''
        Returns a list with all recipe ids in `recipe_ids` that contain any of `allergens`.
        '''
        out = []
        for i in recipe_ids:
            r = self.get_recipe(i)
            if len(set(r.allergens) & set(allergens)) > 0:
                out.append(i)

        return out

    def filter_dislikes(self, recipe_ids: list[int], dislikes: list[str]) -> list[int]:
        '''
        Returns a list with all recipe ids in `recipe_ids` that contain any of `dislikes`.
        '''
        out = []
        for i in recipe_ids:
            r = self.get_recipe(i)

            ingredients = [self.get_dislike_ingredients_by_name(d) for d in dislikes]
            ingredients = [y for x in ingredients for y in x]
            if len(set(r.ingredients) & set(ingredients)) > 0:
                out.append(i)
