import numpy as np
import pandas as pd
from data_ops import standardize
from data_load import DataLoader


# file is responsible for storing ratings given directly by the user
# and convert it to sample data ready for prediction

class UserRating:

    def __init__(self, all_movie_ids):
        self.all_movie_ids = all_movie_ids
        self.rated_movie_ids = list()
        self.ratings = list()

    def add_rating(self, movie_id, rating):
        if movie_id not in self.all_movie_ids:
            raise RuntimeError("Rated movie was unknown")
        if rating not in range(1, 6):
            raise RuntimeError("Rating must be a number 1-5")
        print(movie_id, rating) # TODO remove
        self.rated_movie_ids.append(movie_id)
        self.ratings.append(rating)

    def get_processed_ratings(self):
        # standardize current ratings and initialize panda series for ratings of all movies, set all to 0
        ratings_std = standardize(np.array(self.ratings))
        ratings_series = pd.Series(data=np.zeros(len(self.all_movie_ids)), index=self.all_movie_ids)
        # fill in standardized user ratings
        for movie_id, rating_std in zip(self.rated_movie_ids, ratings_std):
            ratings_series.loc[movie_id] = rating_std

        return ratings_series


if __name__ == "__main__":
    loader = DataLoader()
    X = loader.construct(drop_zero_users=True)
    all_movie_ids = loader.load_movies_with_rating_threshold()
    user_rating = UserRating(all_movie_ids)
    user_rating.add_rating(1, 5)
    user_rating.add_rating(2, 5)
    user_rating.add_rating(3, 3)
    user_rating.add_rating(5, 3)
    print(user_rating.get_processed_ratings())
