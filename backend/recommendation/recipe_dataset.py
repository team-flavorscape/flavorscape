import pickle
import numpy as np

import pandas as pd
from sklearn.decomposition import PCA

class RecipeDataset:
    def __init__(self, path_dataset, normalize=True, dim_reduction='pca', num_components=10):
        with open(path_dataset, 'rb') as file:
            self.raw_data_pd = pickle.load(file)

        self.normalize = normalize
        self.raw_data_pd = (self.raw_data_pd.reset_index()
                            .drop_duplicates(subset='index', keep='last')
                            .set_index('index')
                            .sort_index())

        self.data_pd = self.raw_data_pd
        self.filter_out_empty_recipes_and_attributes(min_entries_attribute=5, min_entries_recipe=10)

        self.model = None
        self.reduced_data_pd = None
        self.data_mean = None
        self.data_std = None
        self.run_dim_reduction(dim_reduction, num_components)

    def filter_out_empty_recipes_and_attributes(self, min_entries_attribute, min_entries_recipe):
        self.data_pd = self.data_pd.drop(self.data_pd.columns[self.data_pd.sum(axis=0) < 2 * min_entries_attribute], axis=1)
        self.data_pd = self.data_pd.drop(self.data_pd.index[self.data_pd.sum(axis=1) < min_entries_recipe], axis=0)
        self.data_pd = self.data_pd.drop(self.data_pd.columns[self.data_pd.sum(axis=0) < min_entries_attribute], axis=1)

    def run_dim_reduction(self, type='pca', num_components=10):
        if type == 'pca':
            alg = self._pca
        else:
            raise NotImplementedError(f'The dimensionality reduction type \"{type}\" has not been implemented.')

        alg(num_components)

    def _pca(self, num_components):
        data_np = self.data_pd.to_numpy()
        if self.normalize:
            self.data_mean = data_np.mean(axis=0)
            self.data_std = data_np.std(axis=0)
            data_np = (data_np - self.data_mean) / self.data_std

        self.model = PCA(n_components=num_components)
        reduced_data_np = self.model.fit_transform(data_np)

        self.reduced_data_pd = pd.DataFrame(reduced_data_np)
        self.reduced_data_pd.index = self.data_pd.index

    def get_recipe(self, recipe):
        return self.data_pd.loc[recipe]

    def get_reduced_recipe(self, recipe):
        return self.reduced_data_pd.loc[recipe]

    def get_closest_recipes(self, recipe_pd: pd.Series):
        recipe_np = recipe_pd.to_numpy().reshape(1, -1)
        if self.normalize:
            recipe_np = (recipe_np - self.data_mean) / self.data_std

        reduced_recipe_np = self.model.transform(recipe_np)
        reduced_recipe_pd = pd.Series(reduced_recipe_np.squeeze())

        diff = self.reduced_data_pd - reduced_recipe_pd
        sq_diff = diff * diff
        return sq_diff.sum(axis=1).sort_values()

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
    recipe = recipe_dataset.get_recipe(recipe_name)
    dist = recipe_dataset.get_closest_recipes(recipe)
    print(dist)

    #reduced_recipe = recipe_dataset.get_reduced_recipe(recipe_name)
    #print(recipe_dataset.get_closest_recipe_to_reduced(reduced_recipe))
