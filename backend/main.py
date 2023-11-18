import json
import random
from fastapi import FastAPI
from pydantic import BaseModel

from recipe import Recipe
from recipes import Recipes
from allergen import Allergen
from dislike import Dislike

# Load recipes from JSON
recipes = None
with open('../data/recipes_10k.json', 'r') as f:
    json_dict = json.load(f)
    recipes = Recipes(json_dict)

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
    return OnboardCheckResponse(isOnboarded=True)

@app.post('/onboard')
def post_onboard(req: OnboardRequest) -> ResultResponse:
    onboardData = req
    print(f'Successful onboarding with allergens {onboardData.allergens} and ingredients {onboardData.dislikes}')
    return ResultResponse(success=True)

@app.get('/allergens')
def get_allergens() -> list[Allergen]:
    return recipes.get_allergens()

@app.get('/ingredients')
def get_ingredients() -> list[Dislike]:
    return recipes.get_dislikes()

@app.get('/ratingRecipes')
def get_rating_recipes() -> list[Recipe]:
    # TODO: Improve sampling for good coverage
    return [recipes.get_recipe(random.randrange(recipes.count())) for i in range(10)]

@app.post('/ratings')
def post_rating(req: list[RatingRequest]) -> ResultResponse:
    # TODO: Implement
    print(f'Received ratings: {req}')
    return ResultResponse(success=True)
