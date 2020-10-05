from config import config
from data_processing.data_load import DataLoader
from recommendation.recommend_movies import MovieRecommender
from data_processing.user_rating import UserRatingHandler

# all logic we need to connect the recommender algorithm to the UI
loader = DataLoader()
recommender = MovieRecommender(loader)
user_rating_handler = UserRatingHandler(loader.load_movies_with_rating_threshold())
movies_to_be_rated = loader.load_most_rated_movies(config.num_of_movies_for_client, shuffle=True)


def get_recommendation_results():
    client_ratings = user_rating_handler.get_processed_ratings()
    return recommender.recommend(client_ratings, n_recommendations=config.num_of_recommendations_for_client)