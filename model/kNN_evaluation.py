import numpy as np
from data_processing.data_load import DataLoader
from model.kNN import UnsupervisedNearestNeighbors
from sklearn.model_selection import train_test_split
from time import time

k = 15      # arbitrary choice for now
X = DataLoader().construct(drop_zero_users=True)
X_train, X_test = train_test_split(X, test_size=0.2)
knn = UnsupervisedNearestNeighbors(k)
knn.fit(X_train)

t0 = time()
X_test_pred = knn.predict(X_test)
t1 = time()
print("predicting took", t1 - t0, "seconds")
mse_row_wise = (np.square(np.subtract(X_test, X_test_pred))).mean(axis=1)
mse = mse_row_wise.mean()
print(mse)

# TODO calculate row-wise mse of X_test and X_test_pred
