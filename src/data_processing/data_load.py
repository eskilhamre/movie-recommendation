import pandas as pd
from data_processing.data_ops import standardize
from sklearn.preprocessing import normalize
from sklearn.utils import shuffle as sklearn_shuffle
from config import config


class DataLoader:

    def __init__(self):
        self.rel_data_path = "data-small/"
        self.n_ratings_threshold = 10  # threshold #ratings a movie must have to be included

    def construct(self, normalize_rows=False, drop_zero_users=False):
        ratings = self.load_ratings()

        # load only movies that has a certain amount of ratings
        exclusive_movie_ids = self.load_movies_with_rating_threshold()
        movies = self.load_movies()
        movies = movies.loc[movies["movieId"].isin(exclusive_movie_ids)]

        # cartesian product of movies, user ratings
        user_rating_product = self.__create_user_rating_product(movies, ratings)

        # standardize cartesian product rows, and replace NaN with zeros
        user_rating_product = user_rating_product.apply(standardize, axis=1).fillna(0)

        # drop users that have rated all movies equally
        if drop_zero_users:
            user_rating_product = user_rating_product.loc[(user_rating_product != 0).any(axis=1), :]

        if normalize_rows:
            user_rating_product = normalize(user_rating_product, axis=1)

        return user_rating_product

    def load_movies(self):
        return pd.read_csv(self.rel_data_path + config.movies_file_name).drop(labels="genres", axis=1)

    def load_ratings(self):
        return pd.read_csv(self.rel_data_path + config.ratings_file_name).drop(labels="timestamp", axis=1)

    def load_most_rated_movies(self, n_movies, shuffle=False):
        """
        Finds the n most rated movies.

        :param n_movies:    number of movies
        :param shuffle:     if True then result is shuffled
        :return:            the n most rated movies, pd dataframe
        """
        movies_df = self.load_movies()

        if n_movies <= 0 or n_movies > len(movies_df):
            raise RuntimeError("Invalid number of movies requested")

        most_rated_movie_ids = self.__load_most_rated_movie_ids(n_movies)
        most_rated_movies = movies_df.loc[movies_df["movieId"].isin(most_rated_movie_ids)].set_index("movieId")

        if shuffle:
            most_rated_movies = sklearn_shuffle(most_rated_movies)
        return most_rated_movies

    def load_movies_with_rating_threshold(self):
        """
        Finds the movies (represented by their ID) that has been rated at least a threshold amount of times.

        :return:                     movie IDs, np array
        """
        rating_counts = self.__load_rating_counts()
        rating_counts = rating_counts[rating_counts >= self.n_ratings_threshold]
        return rating_counts.index

    def __load_most_rated_movie_ids(self, n_movies):
        """
        Finds the n most rated movies, represented by their IDs.

        :param n_movies:
        :return:
        """
        ratings_count = self.__load_rating_counts()
        ratings_count = ratings_count.sort_values(ascending=False)
        return ratings_count.index[:n_movies].to_numpy()

    def __load_rating_counts(self):
        """
        Finds how many times each movie are rated.

        :return: pd series with index=movieId and values=#ratings
        """
        return self.load_ratings().pivot_table(index="movieId", aggfunc="size").rename("Rating counts")

    @staticmethod
    def __create_user_rating_product(movies_df, ratings_df):
        """
        Creates a cartesian product of users (as rows) and movies (as columns), where the (i, j)-value
        is the rating of user i on movie j.
        Certainly not all users has rated all movies, so each such missing field is represented by a NaN.

        :param movies_df:    movies, pd dataframe
        :param ratings_df:   user ratings, pd dataframe
        :return:             Cartesian product, pd dataframe
        """
        movies_ratings_joined = pd.merge(movies_df, ratings_df)
        return movies_ratings_joined.pivot_table(index="userId", columns="movieId", values="rating")


if __name__ == "__main__":
    loader = DataLoader()
    X = DataLoader().construct()
    movieIds = loader.load_movies_with_rating_threshold()
    print(type(movieIds))
    print(X.columns)
    print(movieIds)
    print((X.columns == movieIds).all())
