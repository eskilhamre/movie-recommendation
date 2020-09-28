import pandas as pd
from data_ops import standardize
from sklearn.preprocessing import normalize


class DataLoader:

    def __init__(self):
        self.data_path = "data-small/"
        self.movies_name = "movies.csv"
        self.ratings_name = "ratings.csv"
        self.n_ratings_limit = 10  # threshold #ratings a movie must have to be included

    def construct(self, normalize_rows=False, drop_zero_users=False):
        movies = self.load_movies()
        ratings = self.load_ratings()
        user_rating_product = self.__create_user_rating_product(movies, ratings)

        # drop movies with few ratings, and replace NaN with zeros
        user_rating_product = user_rating_product. \
            dropna(thresh=self.n_ratings_limit, axis=1). \
            apply(standardize, axis=1). \
            fillna(0)

        # if normalize_rows:
        #     user_rating_product = normalize(user_rating_product, axis=1)
        #
        # if drop_zero_users:
        #     # drop users that have rated all movies equally
        #     user_rating_product = user_rating_product.loc[(user_rating_product != 0).any(axis=1), :]
        return user_rating_product

    def load_movies(self):
        return pd.read_csv(self.data_path + self.movies_name).drop(labels="genres", axis=1)

    def load_ratings(self):
        return pd.read_csv(self.data_path + self.ratings_name).drop(labels="timestamp", axis=1)

    @staticmethod
    def __create_user_rating_product(movies_df, ratings_df):
        movies_ratings_joined = pd.merge(movies_df, ratings_df)  # , sort="userId")
        return movies_ratings_joined.pivot_table(values="rating", index="userId", columns="movieId")


if __name__ == "__main__":
    loader = DataLoader()
    df = loader.construct()
    print(df.shape)
    print(df.head(10))
    # sample = df.loc[53]

    # find number of row zero vectors
    count = 0
    for index, row in df.iterrows():
        if (row == 0).all():
            count += 1
    print(count)
