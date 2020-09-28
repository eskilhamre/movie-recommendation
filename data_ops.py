from scipy import spatial
#from data_load import DataLoader
import numpy as np

MAX = 1.0
MIN = -1.0
lol = 1


def cosine_similarities(sample, df):
    """
    Calculates the cosine similarity between the sample vector and all observation rows
    in the pandas DataFrame.
    Essentially, this is how similar the a single user's ratings is to each of the other users.

    :param sample: single observation, mean normalized.
    :param df:     pd dataframe of user-rating cartesian product, each row corresponds to a user, mean normalized
    :return:       pd series of cosine similarity scores, sorted (most similar first)
    """
    if (sample == 0).all():
        # our sample is a zero vector, and is similar only to zero rows (if any)
        similar_score = df.apply(lambda row : MAX if (row == 0).all() else MIN)
    else:
        similar_score = df.apply(lambda row : MAX - spatial.distance.cosine(sample, row), axis=1)
    return similar_score.sort_values(ascending=False, na_position="last")


def standardize(vector):
    """
    Standardize vector: z = vector - mean / std

    :param vector:
    :return: standardized vector z
    """
    z = vector - vector.mean()
    std = vector.std()
    if std != 0:
        z = z / std
    return z
