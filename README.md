# Flavorscape

This project was made for hackaTUM 2023. The challenge posed by HelloFresh was to create a recommender system that generates personalized suggestions for recipes and meals. Based on this, we have explored various ways of ranking dishes based on personal preference, as well as additional features. In the end, we have settled on a solution that we think is both powerful as well as realistic to be implemented within a weekend.

flavorscape automatically assembles weekly meal plans, tailor-made for the taste of its users. Our intuitive onboarding process guides users through the selection of dietary preferences and allergens. Then, a small selection of sample recipes can be rated to build their personal flavor profile.

After less than two minutes, users receive their first suggested weekly meal plan. Unwanted recipes can be discarded and will be replaced by fresh suggestions. This way, a suitable menu can be found in a matter of minutes.

## Usage

### Scraping Recipes

Use the `data/scrape.py` script to fetch recipes from HelloFresh. Create a file in the `data` directory containing your API token. There are some configuration variables at the top of the script.

### Starting the API

Call `uvicorn main:app --reload` in the `backend` directory.

