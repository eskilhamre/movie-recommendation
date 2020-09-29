from data_load import DataLoader
from recommend_movies import MovieRecommender
from user_rating import UserRating
from ui.ui_rater import UIRater

recommender_algorithm = "knn"


class MovieRunnerApplication:

    def __init__(self):
        self.loader = DataLoader()
        self.recommender = MovieRecommender(self.loader, alg=recommender_algorithm)
        self.user_rating = UserRating(self.loader.load_movies_with_rating_threshold())
        self.ui = UIRater(self)

    def run(self):
        self.ui.init_rating()


if __name__ == "__main__":
    app = MovieRunnerApplication()
    app.run()
