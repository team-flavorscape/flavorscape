import pickle
import numpy as np

import pandas as pd
from sklearn.decomposition import PCA

class RecipeDataset:
    def __init__(self, path_dataset, normalize=True, dim_reduction='pca', num_components=20):
        with open(path_dataset, 'rb') as file:
            self.raw_data_pd = pickle.load(file)

        self.normalize = normalize
        self.dim_reduction = dim_reduction
        self.num_components = num_components

        self.raw_data_pd = (self.raw_data_pd.reset_index()
                            .drop_duplicates(subset='index', keep='last')
                            .set_index('index')
                            .sort_index())

        self.add_ingredient_classes()

        self.data_pd = self.raw_data_pd
        self.filter_out_empty_and_normalize(min_entries_attribute=5, min_entries_recipe=10)

        self.model = None
        self.reduced_data_pd = None
        self.data_mean = None
        self.data_std = None
        self.run_dim_reduction(dim_reduction, 25)

    def add_ingredient_classes(self):
        self.alias_ingredient_classes = {
            'beef': [],
            'chicken': [],
            'turkey': [],
            'pork': [],
            'fish': ['salmon', 'tuna'],
            'egg': [],
            'dairy-product': ['milk', 'cheese', 'yoghurt'],
            'bread': [],
            'tortilla': [],
            'pasta': [],
            'rice': [],
            'root-veg': ['potato', 'carrot'],
            'broccoli': ['broccoli', 'cauliflower'],
            'seed': [],
            'legume': ['bean', 'pea'],
            'mushroom': [],
            'nuts': [],
            'cereal': [],
        }

        filter_suffices = ['mix', 'concentrate', 'glace', 'soup', 'sauce']
        filter_prefixes = ['c-', 't-']

        for key, value in self.alias_ingredient_classes.items():
            value.append(key)
            classes = [col for col in self.raw_data_pd.columns if not [s for s in filter_suffices if col.endswith(s)]
                       and not [s for s in filter_prefixes if col.startswith(s)]
                       and [v for v in value if v in col]]
            self.alias_ingredient_classes[key] = classes

        alias_pd = pd.DataFrame(index=self.raw_data_pd.index)
        for key, cols in self.alias_ingredient_classes.items():
            alias_pd.insert(len(alias_pd.columns), key, self.raw_data_pd[cols].any(axis=1).astype('int'))

        self.raw_data_pd = pd.concat([alias_pd, self.raw_data_pd], axis=1)

    def filter_out_recipes(self, recipes):
        self.data_pd.drop(recipes)
        self.run_dim_reduction(self.dim_reduction, self.num_components)

    def filter_out_empty_and_normalize(self, min_entries_attribute, min_entries_recipe):
        self.data_pd = self.data_pd.drop(self.data_pd.columns[self.data_pd.sum(axis=0) < 2 * min_entries_attribute], axis=1)
        self.data_pd = self.data_pd.drop(self.data_pd.index[self.data_pd.sum(axis=1) < min_entries_recipe], axis=0)
        self.data_pd = self.data_pd.drop(self.data_pd.columns[self.data_pd.sum(axis=0) < min_entries_attribute], axis=1)

    def run_dim_reduction(self, type='pca', importance_multiplier=25):
        self.data_mean = self.data_pd.mean(axis=0)
        self.data_std = self.data_pd.std(axis=0)

        if self.normalize:
            self.data_pd = (self.data_pd - self.data_mean) / self.data_std
        else:
            self.data_pd = self.data_pd - self.data_mean

        columns_ingredient_classes = [c for c in self.data_pd.columns if
                                           c in self.alias_ingredient_classes.keys()]
        columns_tag_important = [
            't-spicy',
            't-protein-smart',
            't-calorie-smart',
            't-veggie',
            't-easy',
            't-vegan',
            't-plant-based']
        columns_tag_important = [c for c in self.data_pd.columns if c in columns_tag_important]

        self.data_pd[columns_tag_important] *= importance_multiplier
        self.data_pd[columns_ingredient_classes] *= importance_multiplier

        if type == 'pca':
            alg = self._pca
        else:
            raise NotImplementedError(f'The dimensionality reduction type \"{type}\" has not been implemented.')

        alg(self.num_components)

    def _pca(self, num_components):
        data_np = self.data_pd.to_numpy()

        self.model = PCA(n_components=num_components)
        reduced_data_np = self.model.fit_transform(data_np)

        self.reduced_data_pd = pd.DataFrame(reduced_data_np)
        self.reduced_data_pd.index = self.data_pd.index

    def get_recipe(self, recipe):
        return self.data_pd.loc[recipe]

    def get_reduced_recipe(self, recipe):
        return self.reduced_data_pd.loc[recipe]

    def get_closest_recipes_to_reduced(self, reduced_recipe_pd: pd.Series):
        diff = self.reduced_data_pd - reduced_recipe_pd
        sq_diff = diff * diff
        return sq_diff.sum(axis=1).sort_values()



if __name__ == '__main__':
    recipe_dataset = RecipeDataset('/home/aleks/hackatum/flavorscape/data/recipes_10k.pkl',
                                   normalize=True,
                                   dim_reduction='pca',
                                   num_components=20)

    recipe_name = 'Thai Ginger Curry'
    recipe = recipe_dataset.get_reduced_recipe(recipe_name)
    dist = recipe_dataset.get_closest_recipes_to_reduced(recipe)
    print(dist)

    #reduced_recipe = recipe_dataset.get_reduced_recipe(recipe_name)
    #print(recipe_dataset.get_closest_recipe_to_reduced(reduced_recipe))
