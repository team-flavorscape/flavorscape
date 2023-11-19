import json
from fastapi import FastAPI

from api.app import App
from api.recipes import Recipes

from model.recipe import Recipe
from model.allergen import Allergen
from model.dislike import Dislike

from recommendation.recommendation import Recommendation
from recommendation.recipe_dataset import RecipeDataset

# Load recipes from JSON
recipes = None
with open('../data/recipes_10k.json', 'r') as f:
    json_dict = json.load(f)
    recipes = Recipes(json_dict)

recipe_dataset = RecipeDataset('../data/recipes_10k.pkl', drop_std=0.1)
recommender = Recommendation(recipe_dataset)

# Start API
app = FastAPI()
flavorspaceApp = App(recipes, recommender)
app.include_router(flavorspaceApp.router)

