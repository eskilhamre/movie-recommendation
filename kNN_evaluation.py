from data_load import DataLoader
from kNN import UnsupervisedNearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

k = 10      # arbitrary choice for now
X = DataLoader().construct()
X_train, X_test = train_test_split(X, test_size=0.2)
X_test = X_test.to_numpy()
knn = UnsupervisedNearestNeighbors(k)
knn.fit(X_train)
X_test_pred = knn.predict(X_test)
# TODO calculate row-wise mse of X_test and X_test_pred
