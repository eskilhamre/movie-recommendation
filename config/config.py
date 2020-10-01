# for loading files
movies_file_name = "movies.csv"
ratings_file_name = "ratings.csv"

# unsupervised algorithm to be used for recommendation
recommender_algorithm = "knn"    # only supports knn for now

# k in nearest neighbors
optimal_k = 10                   # choice is arbitrary for now TODO find optimal k with cross validation

# threshold number of ratings a movie must have to be included in recommendation calculations
n_ratings_threshold = 10

# how many movies the client may rate at maximum before recommendation calculation starts
# also, the movies chosen for rating is the {num_of_movies_for_client} most rated ones.
num_of_movies_for_client = 25

# number of movies to recommend the client in the end
num_of_recommendations_for_client = 30