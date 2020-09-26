from data_ops import cosine_similarities
import numpy as np
from data_load import DataLoader


class UnsupervisedNearestNeighbors:

    def __init__(self, k_neighbors):
        self.k_neighbors = k_neighbors
        self.X = None  # pandas df

    def fit(self, X):
        self.X = X

    def predict(self, samples):
        """
        TODO write

        :param samples: numpy array
        :return:
        """
        return np.array([self.predict_single(sample) for sample in samples])

    def predict_single(self, sample):
        """
        TODO write

        :param sample: numpy array
        :return:
        """
        total_similar_score = cosine_similarities(sample, self.X)
        k_similar_score = total_similar_score.iloc[:self.k_neighbors]  # k best similarities scores
        X_alike = self.X.loc[k_similar_score.index]                    # k most similar training samples
        weighted_average = (X_alike.T.dot(k_similar_score)).T / np.sum(k_similar_score)
        return weighted_average.to_numpy()


if __name__ == "__main__":
    X = DataLoader().construct()
    print(X.shape)
    knn = UnsupervisedNearestNeighbors(10)
    knn.fit(X)
    sample = X.iloc[0].to_numpy()     # first row as sample
    sample_pred = knn.predict_single(sample)
    print("Original sample:", sample)
    print("Predicted sample:", sample_pred)
    # samples = X.iloc[:2].to_numpy()
    # samples_pred = knn.predict(samples)
    # print(samples_pred)


