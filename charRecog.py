import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

print digits.data   # features
print digits.target # labels

clf = svm.SVC(gamma = 0.001, C = 100) # specify classifier

X, y = digits.data[:-10], digits.target[:-10] # training set

clf.fit(X, y) # train

print(clf.predict(digits.data[-5])) # test

# lets visualize this
plt.imshow(digits.images[-5], cmap = plt.cm.gray_r, interpolation = 'nearest')
plt.show()
