import pickle
import numpy as np

import pandas as pd
from sklearn.decomposition import PCA

class RecipeDataset:
    def __init__(self, path_dataset, drop_std=1e-6, dim_reduction='pca', num_components=10):
        with open(path_dataset, 'rb') as file:
            self.raw_data_pd = pickle.load(file)

        self.raw_data_pd = (self.raw_data_pd.reset_index()
                            .drop_duplicates(subset='index', keep='last')
                            .set_index('index')
                            .sort_index())

        self.data_pd = None
        self.set_min_std_deviation(std=drop_std)

        self.model = None
        self.reduced_data_pd = None
        self.run_dim_reduction(dim_reduction, num_components)

    def set_min_std_deviation(self, std):
        data_std = self.raw_data_pd.std()
        self.data_pd = self.raw_data_pd.drop(data_std[data_std < std].index.values, axis=1)

    def run_dim_reduction(self, type='pca', num_components=10):
        if type == 'pca':
            self._pca(num_components)
        else:
            raise NotImplementedError(f'The dimensionality reduction type \"{type}\" has not been implemented.')

    def _pca(self, num_components):
        data_np = self.data_pd.to_numpy()
        data_mean = data_np.mean(axis=0)
        data_std = data_np.std(axis=0)
        data_np_norm = (data_np - data_mean) / data_std

        self.model = PCA(n_components=num_components)
        reduced_data_np = self.model.fit_transform(data_np_norm)

        self.reduced_data_pd = pd.DataFrame(reduced_data_np)
        self.reduced_data_pd.index = self.data_pd.index

    def get_recipe(self, recipe):
        return self.data_pd.iloc[recipe]

    def get_distances(self, recipe: str):
        recipe_vector = self.reduced_data_pd.loc[recipe]

        diff = self.reduced_data_pd - recipe_vector
        sq_diff = diff * diff
        return np.sqrt(sq_diff.sum(axis=1))


if __name__ == '__main__':
    recipe_dataset = RecipeDataset('/home/aleks/hackatum/flavorscape/data/recipes_10k.pkl',
                                   drop_std=0.1,
                                   dim_reduction='pca',
                                   num_components=10)

    recipe_name = '\"Little Ears\" Pasta'
    dist = recipe_dataset.get_distances(recipe_name)

    print(dist.sort_values())
