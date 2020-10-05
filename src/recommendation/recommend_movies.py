import pandas as pd
from data_processing.data_load import DataLoader
from model.kNN import UnsupervisedNearestNeighbors
from config import config


class MovieRecommender:

    def __init__(self, data_loader):
        self.data_loader = data_loader

    # noinspection PyMethodMayBeStatic
    def recommend(self, user_ratings, n_recommendations=20):
        """

        :param user_ratings: pd series or np array of standard normalized user ratings
        :param n_recommendations: number of movies to recommend
        :return:
        """
        X = self.data_loader.construct(drop_zero_users=True)
        if len(user_ratings) != X.shape[1]:
            raise RuntimeError("Dimensionality of user ratings do not match dimensionality of training data")
        if n_recommendations <= 0 or n_recommendations >= X.shape[0]:
            raise RuntimeError("Invalid number of recommendations")

        # create model and make prediction
        model = UnsupervisedNearestNeighbors(config.optimal_k)
        model.fit(X)
        prediction = model.predict(user_ratings)
        prediction_df = pd.Series(prediction, index=X.columns, name="predicted rating")    # label predictions with movieIds

        # merge prediction with movies to include movie name, sort on predicted ratings, and pick the n best ones
        movies = self.data_loader.load_movies()
        prediction_movie_name_df = pd.merge(movies, prediction_df, on="movieId")
        prediction_movie_name_df = prediction_movie_name_df.set_index("movieId").sort_values(ascending=False, by="predicted rating")
        return prediction_movie_name_df.head(n_recommendations)


if __name__ == "__main__":
    # get one sample
    loader = DataLoader()
    X = loader.construct(drop_zero_users=True)
    my_user_rating = X.iloc[50]
    recommender = MovieRecommender(loader)
    recommendation = recommender.recommend(my_user_rating, n_recommendations=10)
    #print(recommendation)
    for i, (title, score) in recommendation.iterrows():
        print(i, title, score)

