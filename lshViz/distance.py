# Not used anywhere
from collections import Counter
import numpy as np


class Distance:
    def __init__(self, x):
        self.x = x

    def hamming(self, other):
        diff = self.x ^ other
        return Counter(diff)["1"]

    def cosine(self, other):
        dot_product = np.dot(self.x, other)
        norm_a = np.linalg.norm(self.x)
        norm_b = np.linalg.norm(other)
        return dot_product / (norm_a * norm_b)

    def __lt__(self, other):
        pass
