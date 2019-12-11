import numpy as np
from os import path
from reader import Reader


class LabelReader:
    def __init__(self, *args):
        self.reader = Reader(*args)
        self._labels = None
        self.label_file = f"{self.reader.input_file}"
        self.labels = self.load_labels()

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels

    def cache_labels(self, labels):
        """Saves to binary file"""
        assert not path.isfile(
            f"{self.label_file}.npy"
        ), "Label binary file already exists!"
        print("Writing labels to binary file")
        self.labels = self.reader()
        np.save(self.label_file, self.labels)

    def load_labels(self):
        label_binary_file = f"{self.label_file}.npy"
        if path.isfile(label_binary_file):
            print("Loading labels from binary file")
            return np.load(label_binary_file)
        else:
            labels = self.reader()
            self.cache_labels(labels)
            return labels


if __name__ == "__main__":
    raw_reader = LabelReader("../examples/mnist/mnist_train_labels")
    print(raw_reader.labels)
