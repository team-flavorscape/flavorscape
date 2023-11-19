import pandas as pd
from recipe_dataset import RecipeDataset
from sklearn.cluster import KMeans

#from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor


class Recommendation:
    def __init__(self, recipe_dataset: RecipeDataset, n_neighbours=5):
        self.recipe_dataset = recipe_dataset

        self.ratings = pd.Series()
        #self.model = KNeighborsRegressor(n_neighbors=n_neighbours, weights='distance')
        self.model = RandomForestRegressor(max_depth=5, random_state=0)

    def get_representative_samples(self, num_samples):
        X = self.recipe_dataset.reduced_data_pd.to_numpy()
        kmeans = KMeans(n_clusters=num_samples, random_state=None, n_init="auto").fit(X)

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
                                   normalize=True,
                                   dim_reduction='pca',
                                   num_components=10)

    recommendation = Recommendation(recipe_dataset, n_neighbours=5)

    #for rec in recommendation.get_representative_samples(num_samples=20):
    #    print(f'\'{rec}\': ,')

    onboardings = pd.Series({'Barramundi and Scallion Sriracha Pesto':      -1,
                             'Speedy Steak Fajitas':                        -1,
                             'Deli-Style Turkey Wraps':                     -1,
                             'Smoky Apple Chicken':                         -1,
                             'Creamy Chicken Sausage Tortelloni Limone':    -1,
                             'Churro Waffle & Bacon Brunch Board':          -1,
                             'Middle Eastern Steak Bowls':                  -1,
                             'Sweet & Spicy Pork Noodle Stir-Fry':          -1,
                             'BBQ Pork Burgers':                            -1,
                             'One-Pan Moo Shu Pork Bowls':                  -1,
                             'Zucchini & Sun-Dried Tomato Panini':          1,
                             'Saucy Thyme Steak':                           -1,
                             'Crispy Chickpea Tacos':                       1,
                             'Pork Schnitzel':                              -1,
                             'Pho-Style Beef Noodle Soup':                  -1,
                             'Turkey Patties with Smoky Lemon Crema':       -1,
                             'Fully Loaded Pork Taquitos':                  -1,
                             'Breakfast Chorizo, Kale, and Tomato Skillet': 1,
                             'Cauliflower & Chickpea Tikka Masala':         1,
    })

    recommendation.add_ratings(onboardings)

    recipes = list(recipe_dataset.reduced_data_pd.index)

    predictions_np = recommendation.get_prediction(recipe_dataset.get_reduced_recipe(recipes).to_numpy())
    result_pd = pd.Series(predictions_np, index=recipes).sort_values(ascending=False)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(result_pd.drop(onboardings.index))

