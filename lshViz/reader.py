import numpy as np


class Reader:
    def __init__(self, input_file=None, delimiter=","):
        self.input_file = input_file
        self.delimiter = delimiter

    def __call__(self):
        return np.loadtxt(self.input_file, delimiter=self.delimiter)
