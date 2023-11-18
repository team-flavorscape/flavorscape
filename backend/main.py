import json
import random
from fastapi import FastAPI
from pydantic import BaseModel

from recipes import Recipes

from api.recipe import Recipe
from api.allergen import Allergen
from api.dislike import Dislike

from recommendation.recommendation import Recommendation
from recommendation.recipe_dataset import RecipeDataset

g_onboarded = False

# Load recipes from JSON
recipes = None
with open('../data/recipes_10k.json', 'r') as f:
    json_dict = json.load(f)
    recipes = Recipes(json_dict)

recipe_dataset = RecipeDataset('../data/recipes_10k.pkl')
recommender = Recommendation(recipe_dataset)

app = FastAPI(swagger_ui_parameters={})

class OnboardCheckResponse(BaseModel):
    isOnboarded: bool

class OnboardRequest(BaseModel):
    allergens: list[int] | None = []
    dislikes: list[int] | None = []

class RatingRequest(BaseModel):
    recipe_id: int
    rating: int

class ResultResponse(BaseModel):
    success: bool

onboardData: OnboardRequest

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/onboardCheck')
def get_onboard_check() -> OnboardCheckResponse:
    return OnboardCheckResponse(isOnboarded=g_onboarded)

@app.post('/onboard')
def post_onboard(req: OnboardRequest) -> ResultResponse:
    onboardData = req
    print(f'Successful onboarding with allergens {[recipes.get_allergen_name(a) for a in onboardData.allergens]} and ingredients {[recipes.get_dislike_name(i) for i in onboardData.dislikes]}')
    return ResultResponse(success=True)

@app.get('/allergens')
def get_allergens() -> list[Allergen]:
    return recipes.get_allergens()

@app.get('/ingredients')
def get_ingredients() -> list[Dislike]:
    return recipes.get_dislikes()

@app.get('/ratingRecipes')
def get_rating_recipes() -> list[Recipe]:
    return [recipes.get_recipe_by_name(n) for n in recommender.get_representative_samples(10)]

@app.post('/ratings')
def post_rating(req: list[RatingRequest]) -> ResultResponse:
    global g_onboarded
    # TODO: Implement
    print(f'Received ratings: {req}')
    g_onboarded = True
    return ResultResponse(success=True)

@app.get('/recommendedRecipes')
def get_recommended_recipes(count: int) -> list[Recipe]:
    # TDOO: Implement
    return []
