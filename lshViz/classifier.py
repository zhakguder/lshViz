from sklearn.neighbors import KNeighborsClassifier


class Classifier:
    def __init__(self, training_features, training_labels, n_neighbors):

        self.classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.model = self.classifier.fit(training_features, training_labels)

    def predict(self, new_point):
        features = new_point.__dict__[new_point.classification_attribute].reshape(1, -1)
        label = new_point.label
        return self.model.predict(features)


if __name__ == "__main__":
    from ipdb import set_trace

    X = [[0], [1], [2], [3]]
    y = [0, 0, 1, 1]
    set_trace()
    res = classify(X, y, 2)
