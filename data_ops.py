from scipy import spatial
from data_load import DataLoader


def cosine_similarities(sample, df):
    """
    Calculates the cosine similarity between the sample vector and all observation rows
    in the pandas DataFrame.
    Essentially, this is how similar the a single user's ratings is to each of the other users.

    :param sample: single observation, mean normalized.
    :param df:     pd dataframe of user-rating cartesian product, each row corresponds to a user, mean normalized
    :return:       pd series of cosine similarity scores, sorted (most similar first)
    """
    # cosine distance increases as the angle increases, so therefore we subtract it from 1
    similar_score = df.apply(lambda row: 1 - spatial.distance.cosine(sample, row), axis=1)
    return similar_score.sort_values(ascending=False)


if __name__ == "__main__":
    df = DataLoader().construct()
    sample = df.iloc[0]
    sim = cosine_similarities(sample, df)
    sim_head = sim.iloc[:10]
    print(sim_head)
