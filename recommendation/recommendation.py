import pandas as pd
from recipe_dataset import RecipeDataset
from sklearn.cluster import KMeans

class Recommendation:
    def __init__(self, recipe_dataset: RecipeDataset):
        self.recipe_dataset = recipe_dataset

    def get_representative_samples(self, num_samples):
        X = self.recipe_dataset.reduced_data_pd.to_numpy()
        kmeans = KMeans(n_clusters=num_samples, random_state=0, n_init="auto").fit(X)

        representative_samples = []
        for cluster_center in kmeans.cluster_centers_:
            representative_samples.append(self.recipe_dataset.get_closest_recipes_to_reduced(pd.Series(cluster_center))
                                          .index[0])

        return representative_samples

if __name__ == '__main__':
    recipe_dataset = RecipeDataset('/home/aleks/hackatum/flavorscape/data/recipes_10k.pkl',
                                   drop_std=0.1,
                                   normalize=True,
                                   dim_reduction='pca',
                                   num_components=20)

    recommendation = Recommendation(recipe_dataset)
    print(recommendation.get_representative_samples(10))

    print(recipe_dataset.get_closest_recipes(recipe_dataset.get_recipe('Vibrant Veggie Skewers')))