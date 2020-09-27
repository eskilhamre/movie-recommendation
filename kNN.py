from data_ops import cosine_similarities
import numpy as np
from data_load import DataLoader


class UnsupervisedNearestNeighbors:

    def __init__(self, k_neighbors):
        self.k_neighbors = k_neighbors
        self.X = None                  # pandas df
        self.column_labels = None

    def fit(self, X):
        """
        TODO write

        :param X: pandas df
        :return:
        """
        self.X = X
        self.column_labels = X.columns

    def predict(self, samples):
        """
        TODO write

        :param samples: pandas df
        :return: numpy array
        """
        return np.array([self.predict_single(sample) for index, sample in samples.iterrows()])

    def predict_single(self, sample):
        """
        TODO write

        :param sample: pandas df or numpy array
        :return: numpy array
        """
        total_similar_score = cosine_similarities(sample, self.X)
        k_similar_score = total_similar_score.iloc[:self.k_neighbors]  # k best similarities scores
        X_alike = self.X.loc[k_similar_score.index]                    # k most similar training samples
        weighted_average = (X_alike.T.dot(k_similar_score)).T / np.sum(k_similar_score)
        return weighted_average.to_numpy()


if __name__ == "__main__":
    X = DataLoader().construct()
    knn = UnsupervisedNearestNeighbors(4)
    knn.fit(X)
    # sample = X.iloc[0]     # first row as sample
    # sample_pred = knn.predict_single(sample)
    # print("Original sample:", sample)
    # print("Predicted sample:", sample_pred)
    samples = X.iloc[:2]
    samples_pred = knn.predict(samples)
    print(samples_pred)


