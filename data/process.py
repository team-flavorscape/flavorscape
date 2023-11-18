#!/usr/bin/env python

import datetime
import pandas as pd
import json

IN_FILE = 'recipes_10k.json'

recipes = []

print(f'Loading {IN_FILE}...')
with open(IN_FILE, 'r') as f:
    recipes = json.load(f)

print(f'Loaded {len(recipes)} recipes.')

ingredients = []
tags = []
cuisines = []

# Initialize columns for dataframe
for r in recipes:
    for i in r['ingredients']:
        ingredients.append(i['slug']) if i['slug'] not in ingredients else ingredients
    for t in r['tags']:
        tags.append('t-' + t['slug']) if 't-' + t['slug'] not in tags else tags
    for c in r['cuisines']:
        cuisines.append('c-' + c['slug']) if 'c-' + c['slug'] not in cuisines else cuisines

data = {}
indices = []

# Initialize arrays in dataframe columns
for i in ingredients:
    data[i] = []

for t in tags:
    data[t] = []

for c in cuisines:
    data[c] = []

# Generate dataframe dict
for r in recipes:
    indices.append(r['name'])
    for y in range(len(ingredients)):
        data[ingredients[y]].append(0)
        for i in r['ingredients']:
            if i['slug'] == ingredients[y]:
                data[ingredients[y]][-1] = 1

    for y in range(len(tags)):
        data[tags[y]].append(0)
        for t in r['tags']:
            if 't-' + t['slug'] == tags[y]:
                data[tags[y]][-1] = 1

    for y in range(len(cuisines)):
        data[cuisines[y]].append(0)
        for c in r['cuisines']:
            if 'c-' + c['slug'] == cuisines[y]:
                data[cuisines[y]][-1] = 1

d = pd.DataFrame(data, index=indices)
d.to_pickle('recipes.pkl')
