import numpy as np

from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split

# do a binary digit classification
digits = load_digits()
X, y = digits.data, digits.target

# make binary task by doing odd vs even numers
y = y % 2
# code as +1 and -1
y = 2 * y - 1
X /= X.max()

X_train, X_test, y_train, y_test = train_test_split(X, y)
X_train_bias = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
X_test_bias = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
print  "cenas"