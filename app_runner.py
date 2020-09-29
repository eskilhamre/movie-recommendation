from data_load import DataLoader
from recommend_movies import MovieRecommender
from user_rating import UserRating
from ui.ui_rater import UIRater


class RecommendationApplication:

    def __init__(self):
        self.loader = DataLoader()
        self.recommender = MovieRecommender(self.loader)
        self.user_rating = UserRating(self.loader.load_movies_with_rating_threshold())
        self.ui = UIRater(self)

    def run(self):
        self.ui.init_rating()


if __name__ == "__main__":
    app = RecommendationApplication()
    app.run()
