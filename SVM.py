import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier


class SVM:

    def __init__(self):
        initial = [[[0.2, 0.553519174456596], [0]],
                   [[0.3, 0.830065906047821], [1]],
                   [[0.2, 0.999999940395355], [1]],
                   [[0.15, 0.983746290206909], [1]],
                   [[0.5, 1.0], [1]],
                   [[1, 0.3], [1]],
                   [[1, 0.6], [1]],
                   [[1, 0.8], [1]],
                   [[0.9, 0.785746290206909], [1]],
                   [[0.1, 0.960313141345978], [0]],
                   [[0.04, 0.4], [0]],
                   [[0.1, 0.4], [0]],
                   [[0.3, 0.4], [0]],
                   [[0.6, 0.4], [0]],
                   [[0.6, 0.7854], [0]],
                   [[0.45, 0.68], [0]],
                   [[0.1, 0.985110819339752], [0]]]

        Xs = []
        ys = []
        for i in initial:
            Xs.append(i[0])
            ys.append(i[1])
        self.X = np.array(Xs)
        self.y = np.array(ys)
        
    def classifyBySVCPolynomialKernel(self, vectorTobeClassified):
        C = 1.0  # SVM regularization parameter

        clf = svm.SVC(kernel="poly", degree=3, gamma="auto", C=C).fit(self.X, self.y)
        return clf.predict(vectorTobeClassified)

    def classifyBySVCRBFKernel(self, vectorTobeClassified):
        C = 1.0  # SVM regularization parameter

        clf = svm.SVC(kernel="rbf", gamma=0.9, C=C).fit(self.X, self.y)
        return clf.predict(vectorTobeClassified)

    def classifyByNearestNeighbours(self, vectorTobeClassified):
        C = 1.0  # SVM regularization parameter

        clf = KNeighborsClassifier(3).fit(self.X, self.y)
        return clf.predict(vectorTobeClassified)

    def classifyByWeightedSVM(self, vectorTobeClassified):
        X = np.array([[0.2, 0.553519174456596],
                      [0.3, 0.830065906047821],
                      [0.2, 0.999999940395355],
                      [0.15, 0.983746290206909],
                      [0.5, 1.0],
                      [0.1, 0.960313141345978],
                      [0.04, 0.4],
                      [0.1, 0.985110819339752]])
        y = np.array([0, 1, 0, 1, 1, 1, 0, 0])
        print(X)
        print(y)

        clf_weights = svm.SVC(gamma=1)
        clf_weights.fit(X, y)

        clf_no_weights = svm.SVC(gamma=1)
        clf_no_weights.fit(X, y)




