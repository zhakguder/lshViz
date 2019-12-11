from reader import Reader
from os import path
import numpy as np

"""
class RawVectorReader:
    def __init__(self, *args):
        self.reader = Reader(*args)
        self._vectors = self.reader()

    @property
    def vectors(self):
        return self._vectors
"""


class RawVectorReader:
    def __init__(self, *args):
        self.reader = Reader(*args)
        self._vectors = None
        self.vector_file = f"{self.reader.input_file}"
        self.vectors = self.load_vectors()

    @property
    def vectors(self):
        return self._vectors

    @vectors.setter
    def vectors(self, vectors):
        self._vectors = vectors

    def cache_vectors(self, vectors):
        """Saves to binary file"""
        assert not path.isfile(
            f"{self.vector_file}.npy"
        ), "Feature binary file already exists!"
        self.vectors = self.reader()
        print("Writing features to binary file")
        np.save(self.vector_file, self.vectors)

    def load_vectors(self):
        vector_binary_file = f"{self.vector_file}.npy"
        if path.isfile(vector_binary_file):
            print("Loading vectors from binary file")
            return np.load(vector_binary_file)
        else:
            vectors = self.reader()
            self.cache_vectors(vectors)
            return vectors


if __name__ == "__main__":
    raw_reader = RawVectorReader("../examples/mnist/mnist_train_feature")
    print(raw_reader.vectors)
