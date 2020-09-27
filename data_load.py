import pandas as pd
from data_ops import std_normalize


class DataLoader:

    def __init__(self):
        self.data_path = "data-small/"
        self.movies_name = "movies.csv"
        self.ratings_name = "ratings.csv"
        self.n_ratings_limit = 10  # threshold #ratings a movie must have to be included

    def construct(self, drop_zero_users=False):
        movies = self.load_movies(self.movies_name, self.data_path)
        ratings = self.load_ratings(self.ratings_name, self.data_path)
        user_rating_product = self._create_user_rating_product(movies, ratings)

        # drop movies with few ratings, normalize each row such that row mean is 0, and replace NaN with zeros
        user_rating_product = user_rating_product. \
            dropna(thresh=self.n_ratings_limit, axis=1). \
            apply(std_normalize, axis=1). \
            fillna(0)

        if drop_zero_users:
            # drop users that have rated all movies equally
            user_rating_product = user_rating_product.loc[(user_rating_product != 0).any(axis=1), :]
        return user_rating_product

    @staticmethod
    def load_movies(name, rel_path):
        return pd.read_csv(rel_path + name).drop(labels="genres", axis=1)

    @staticmethod
    def load_ratings(name, rel_path):
        return pd.read_csv(rel_path + name).drop(labels="timestamp", axis=1)

    @staticmethod
    def _create_user_rating_product(movies_df, ratings_df):
        movies_ratings_joined = pd.merge(movies_df, ratings_df)  # , sort="userId")
        return movies_ratings_joined.pivot_table(values="rating", index="userId", columns="movieId")


if __name__ == "__main__":
    loader = DataLoader()
    df = loader.construct()
    print(df.head(10))
    # sample = df.loc[53]
    count = 0
    for index, row in df.iterrows():
        if (row == 0).all():
            count += 1
    print(count)
