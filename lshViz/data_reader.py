import os


class DataReader:
    def __init__(self, input_file=None):
        self.input_file = input_file
        self.output_dir = os.path.dirname(input_file)
        self._labels = None
        self._raw_vectors_reader = None
        self._prepare_raw_data()

    def _prepare_raw_data(self):
        raise NotImplementedError

    @property
    def label_reader(self):
        return self._label_reader

    @label_reader.setter
    def label_reader(self, label_reader):
        self._label_reader = label_reader

    @property
    def raw_vector_reader(self):
        return self._raw_vector_reader

    @raw_vector_reader.setter
    def raw_vector_reader(self, raw_vector_reader):
        self._raw_vector_reader = raw_vector_reader


if __name__ == "__main__":
    dr = DataReader()
