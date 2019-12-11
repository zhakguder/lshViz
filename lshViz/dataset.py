from data_reader import DataReader
from mnist_reader import MnistReader
from point import Point
from util import one_vs_all, get_sized_random_subset
from classifier import Classifier

from ipdb import set_trace


class Dataset:
    def __init__(self, data_reader=DataReader, per_label_dataset_size=10):
        self.data_reader = data_reader()
        self.per_label_dataset_size = per_label_dataset_size

        self.features_ = self.data_reader.raw_vector_reader.vectors
        self.labels_ = self.data_reader.label_reader.labels
        keep_indices = self._get_keep_indices()
        self.points = [
            Point(*val, ind)
            for ind, val in enumerate(zip(self.features_, self.labels_))
            if ind in keep_indices
        ]
        del self.features_
        self._features = None
        del self.labels_
        self._labels = None
        del self.data_reader

    def _get_keep_indices(self):
        return get_sized_random_subset(self.labels_, self.per_label_dataset_size)

    def preprocess_features(self):
        pass

    def process_features(self):
        raise NotImplementedError

    def process_labels(self):
        pass

    def __iter__(self):
        return self.points.__iter__()

    def __getitem__(self, ind):
        return self.points[ind]

    def __len__(self):
        return len(self.points)

    def classify_points(self, attr, n_neighbors):
        training_features = self.features if attr == "features" else self.__dict__[attr]
        training_labels = [point.label for point in self]
        self.classifier = Classifier(training_features, training_labels, n_neighbors)

    @property
    def features(self):
        return [point.features for point in self]

    @property
    def labels(self):
        return [point.label for point in self]

    def one_vs_rest_labels(self, query_label):
        """Given a query label returns a new list of labels indicating class
        membership to the query label of each point in the dataset"""
        labels = [point.label for point in self]

        return one_vs_all(labels, query_label)


if __name__ == "__main__":
    ds = Dataset(MnistReader)
    for f, l in ds:
        print(f"l: {l}")
        print(f"f: {f[0]}")
