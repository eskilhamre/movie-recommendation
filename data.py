import pandas as pd
import numpy as np

data_path = "data-small/"
movies_name = "movies.csv"
ratings_name = "ratings.csv"
n_ratings_limit = 10  # threshold #ratings a movie must have to be included


def create_user_rating_product():
    movies = load_movies(movies_name, data_path)
    ratings = load_ratings(ratings_name, data_path)
    user_rating_product = _create_user_rating_product(movies, ratings)

    # drop movies with few ratings, normalize each row such that row mean is 0, and replace NaN with zeros
    user_rating_product = user_rating_product. \
        dropna(thresh=n_ratings_limit, axis=1). \
        apply(_normalize_row, axis=1). \
        fillna(0)
    return user_rating_product


def load_movies(name, rel_path):
    return pd.read_csv(rel_path + name).drop(labels="genres", axis=1)


def load_ratings(name, rel_path):
    return pd.read_csv(rel_path + name).drop(labels="timestamp", axis=1)


def _normalize_row(row):
    return (row - np.mean(row)) / (row.max() - row.min())


def _create_user_rating_product(movies_df, ratings_df):
    movies_ratings_joined = pd.merge(movies_df, ratings_df)  # , sort="userId")
    return movies_ratings_joined.pivot_table(values="rating", index="userId", columns="movieId")


if __name__ == "__main__":
    df = create_user_rating_product()
    print(df.head())
