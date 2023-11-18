#!/usr/bin/env python

import requests
import json
import datetime

N_RECIPES = 10000
BATCH_SIZE = 250
OUT_FILE = 'recipes.json'
skip = 0

# Load API token
TOKEN=''
with open('.api_token', 'r') as f:
    TOKEN=f.read()

recipes = []

while len(recipes) < N_RECIPES:
    URL = f'https://www.hellofresh.com/gw/recipes/recipes/search?country=US&locale=en-US&min-rating=3.3&skip={skip}&sort=-favorites&take={BATCH_SIZE}'
    print(f'Fetching {URL}...', end='', flush=True)
    x = requests.get(URL, headers={'Authorization': f'Bearer {TOKEN}'}).json()
    print(' Done.')

    recipes.extend(x['items'])
    if x['count'] < BATCH_SIZE:
        print('No more elements left to fetch, stopping')
        break
    skip = skip + BATCH_SIZE

print(f'Fetched {len(recipes)} recipes, ')

# Find duplicate recipes and remove all but the most recent one
recipes_dedup = {}
for r in recipes:
    name = r['name']
    if name in recipes_dedup:
        a = datetime.datetime.fromisoformat(r['createdAt'])
        b = datetime.datetime.fromisoformat(recipes_dedup[name]['createdAt'])
        if a > b:
            recipes_dedup[name] = r
    else:
        recipes_dedup[name] = r

recipes = list(recipes_dedup.values())

print(f'{len(recipes)} recipes left after deduplication saving to {OUT_FILE}...')

with open(OUT_FILE, 'w') as f:
    json.dump(recipes, f)

