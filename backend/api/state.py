from model.recipe import Recipe
from model.allergen import Allergen
from model.dislike import Dislike

RECIPE_HISTORY_COUNT = 30

class State:
    onboarded: bool
    recipe_history: list[int] # List of recipe indices
    current_weekly_plan: list[Recipe]
    user_allergens: list[Allergen]
    user_dislikes: list[Dislike]
    
    def __init__(self):
        self.onboarded = False
        self.recipe_history = []
        self.current_weekly_plan = []
        self.user_allergens = []
        self.user_dislikes = []

    def add_recipes_to_history(self, recipe_ids: list[int]):
        for i in recipe_ids:
            self.recipe_history.append(i)

        while len(self.recipe_history) > RECIPE_HISTORY_COUNT:
            self.recipe_history.pop(0)

    def set_weekly_plan(self, recipes: list[Recipe]):
        self.current_weekly_plan = recipes

    def get_recency_penalties(self, indices: list[int]):
        penalties = []
        for i in indices:
            try:
                pos = self.recipe_history.index(i)
                pen = -0.5 * (pos / RECIPE_HISTORY_COUNT)
                penalties.append(pen)
            except ValueError:
                penalties.append(0)

        return penalties
