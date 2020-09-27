from data_load import DataLoader
from kNN import UnsupervisedNearestNeighbors


class MovieRecommender:

    def __init__(self):
        pass

    def recommend(self, user_ratings, alg="knn"):
        """

        :param user_ratings: pd series of raw user ratings
        :param alg:
        :return:
        """