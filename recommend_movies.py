import pandas as pd
from data_load import DataLoader
from kNN import UnsupervisedNearestNeighbors

# noinspection PyRedundantParentheses
valid_algs = ("knn")
optimal_k = 10  # choice is arbitrary for now TODO find optimal k with cross validation


class MovieRecommender:

    def __init__(self, data_loader, alg="knn"):
        if alg not in valid_algs:
            raise RuntimeError("Invalid recommendation algorithm")
        self.data_loader = data_loader
        self.alg = alg

    # noinspection PyMethodMayBeStatic
    def recommend(self, user_ratings, n_recommendations=20):
        """

        :param user_ratings: pd series or np array of standard normalized user ratings
        :param alg:
        :param n_recommendations: number of movies to recommend
        :return:
        """
        X = self.data_loader.construct(drop_zero_users=True)
        if len(user_ratings) != X.shape[1]:
            raise RuntimeError("Dimensionality of user ratings do not match dimensionality of training data")
        if n_recommendations <= 0 or n_recommendations >= X.shape[0]:
            raise RuntimeError("Invalid number of recommendations")

        # create model and make prediction
        model = UnsupervisedNearestNeighbors(optimal_k)
        model.fit(X)
        prediction = model.predict(user_ratings)
        prediction_df = pd.Series(prediction, index=X.columns, name="predicted rating")    # label predictions with movieIds

        # merge prediction with movies to include movie name, sort on predicted ratings, and pick the n best ones
        movies = self.loader.load_movies()
        prediction_movie_name_df = pd.merge(movies, prediction_df, on="movieId")
        prediction_movie_name_df = prediction_movie_name_df.set_index("movieId").sort_values(ascending=False, by="predicted rating")
        return prediction_movie_name_df.head(n_recommendations)


if __name__ == "__main__":
    X = DataLoader().construct(drop_zero_users=True)
    my_user_rating = X.iloc[50]
    print(my_user_rating.sort_values(ascending=False).head(20), end="\n\n")
    recommender = MovieRecommender("knn")
    recommendation = recommender.recommend(my_user_rating, n_recommendations=10)
    print(recommendation)

