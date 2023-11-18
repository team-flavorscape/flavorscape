import pandas as pd
from recipe_dataset import RecipeDataset
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor


class Recommendation:
    def __init__(self, recipe_dataset: RecipeDataset, n_neighbours=5):
        self.recipe_dataset = recipe_dataset

        self.ratings = pd.Series()
        self.model = KNeighborsRegressor(n_neighbors=n_neighbours, weights='distance')

    def get_representative_samples(self, num_samples):
        X = self.recipe_dataset.reduced_data_pd.to_numpy()
        kmeans = KMeans(n_clusters=num_samples, random_state=0, n_init="auto").fit(X)

        representative_samples = []
        for cluster_center in kmeans.cluster_centers_:
            representative_samples.append(self.recipe_dataset.get_closest_recipes_to_reduced(pd.Series(cluster_center))
                                          .index[0])

        return representative_samples

    def add_ratings(self, ratings: pd.Series):
        self.ratings = pd.concat([self.ratings, ratings])
        grouped_ratings = self.ratings.groupby(level=0).mean()
        grouped_ratings_np = grouped_ratings.to_numpy()
        grouped_recipes_np = self.recipe_dataset.get_reduced_recipe(grouped_ratings.index).to_numpy()
        self.model.fit(grouped_recipes_np, grouped_ratings_np)

    def get_prediction(self, reduced_recipes):
        return self.model.predict(reduced_recipes)


if __name__ == '__main__':
    recipe_dataset = RecipeDataset('/home/aleks/hackatum/flavorscape/data/recipes_10k.pkl',
                                   drop_std=0.1,
                                   normalize=True,
                                   dim_reduction='pca',
                                   num_components=20)

    recommendation = Recommendation(recipe_dataset, n_neighbours=5)
    recommendation.add_ratings(pd.Series({'Al Pastor Pork': 1,
                                          'A Caesar Salad to Rule Them All': -1,
                                          'Apple Crisps': -1,
                                          'Apricot Pork Cutlets': 1,
                                          'Asian Pork Wraps': 1,
                                          'Asparagus Risotto': -1,
                                          'Pork Fajitas': 1,
                                          'Roasted Veggie Kale Salad': -1}))

    recipes = recipe_dataset.reduced_data_pd.index
    predictions_np = recommendation.get_prediction(recipe_dataset.get_reduced_recipe(recipes).to_numpy())
    result_pd = pd.Series(predictions_np, index=recipes).sort_values(ascending=False)

    print(result_pd)

