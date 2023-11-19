from fastapi import APIRouter
import pandas as pd
import numpy as np

from recommendation.recommendation import Recommendation
from api.state import State
from api.api_types import *
from api.recipes import Recipes

from model.allergen import Allergen
from model.recipe import Recipe
from model.dislike import Dislike

class App:
    recipes: Recipes
    recommender: Recommendation

    def __init__(self, recipes, recommender):
        self.state = State()
        self.recipes = recipes
        self.recommender = recommender
        self.router = APIRouter()

        self.router.add_api_route('/', self.read_root, methods=['GET'])
        self.router.add_api_route('/onboardCheck', self.get_onboard_check, methods=['GET'])
        self.router.add_api_route('/onboard', self.post_onboard, methods=['POST'])
        self.router.add_api_route('/allergens', self.get_allergens, methods=['GET'])
        self.router.add_api_route('/ingredients', self.get_ingredients, methods=['GET'])
        self.router.add_api_route('/ratingRecipes', self.get_rating_recipes, methods=['GET'])
        self.router.add_api_route('/ratings', self.post_ratings, methods=['POST'])
        self.router.add_api_route('/recommendedRecipes', self.get_recommended_recipes, methods=['GET'])
        self.router.add_api_route('/weeklyPlan', self.post_weekly_plan, methods=['POST'])
        self.router.add_api_route('/weeklyPlan', self.get_weekly_plan, methods=['GET'])

    def read_root(self):
        return {"Hello": "World"}

    def get_onboard_check(self) -> OnboardCheckResponse:
        return OnboardCheckResponse(isOnboarded=self.state.onboarded)

    def post_onboard(self, req: OnboardRequest) -> ResultResponse:
        onboardData = req
        print(f'Successful onboarding with allergens {[self.recipes.get_allergen_name(a) for a in onboardData.allergens]} and ingredients {[self.recipes.get_dislike_name(i) for i in onboardData.dislikes]}')
        return ResultResponse(success=True)

    def get_allergens(self) -> list[Allergen]:
        return self.recipes.get_allergens()

    def get_ingredients(self) -> list[Dislike]:
        return self.recipes.get_dislikes()

    def get_rating_recipes(self) -> list[Recipe]:
        recipes = [self.recipes.get_recipe_by_name(n) for n in self.recommender.get_representative_samples(10)]
        self.state.add_recipes_to_history([r.id for r in recipes])
        return recipes

    def post_ratings(self, req: list[RatingRequest]) -> ResultResponse:
        print(f'Received ratings: {req}')
        self.state.onboarded = True

        s = pd.Series({self.recipes.get_recipe(r.recipe_id).name : r.rating for r in req})
        self.recommender.add_ratings(s)

        return ResultResponse(success=True)

    def get_recommended_recipes(self, count: int) -> list[Recipe]:
        names = [self.recipes.get_recipe(i).name for i in range(self.recipes.count())]
        reduced_recipes = self.recommender.recipe_dataset.get_reduced_recipe(names).to_numpy()
        preds = self.recommender.get_prediction(reduced_recipes)
        print(preds)
        penalties = np.array(self.state.get_recency_penalties([i for i in range(self.recipes.count())]), dtype='float64')
        print(penalties)
        preds += penalties
        print(preds)

        indices = np.argsort(preds)[-count:].tolist()
        self.state.add_recipes_to_history(indices)
        return [self.recipes.get_recipe(i) for i in indices]

    def post_weekly_plan(self, req: list[WeeklyPlanRequest]) -> ResultResponse:
        self.state.set_weekly_plan([self.recipes.get_recipe(r.recipe_id) for r in req])
        return ResultResponse(success=True)

    def get_weekly_plan(self) -> list[Recipe]:
        return self.state.current_weekly_plan