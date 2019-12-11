from bucket import BucketSet
from ipdb import set_trace
from math import ceil
from itertools import chain
import numpy as np
from operator import itemgetter
from collections import Counter


class Point:
    def __init__(self, features=None, label=None, index=None):
        self.features = features
        self.label = label
        self.index = index
        self.dataset = None
        self._classification_attribute = None

    def __lt__(self, other):
        return self.index < other.index

    def filter_label(self, label):
        return self.label == label

    @property
    def classification_attribute(self):
        return self._classification_attribute

    @classification_attribute.setter
    def classification_attribute(self, attr):
        self._classification_attribute = attr

    def predict_class(self):
        return self.dataset.classifier.predict(self)


class HashPoint(Point):
    def __init__(self, point=None, features=None, label=None, index=None):
        if not isinstance(point, Point):
            super().__init__(features, label, index)
        else:
            self.features, self.label, self.index = (
                point.features,
                point.label,
                point.index,
            )
        self._buckets = []

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_buckets"]
        return state

    def __setstate__(self, state):
        state["_buckets"] = []
        self.__dict__ = state

    @property
    def buckets(self):
        return self._buckets

    @buckets.setter
    def buckets(self, bucket):
        bucket.add_point(self)
        self._buckets.append(bucket)

    def _neighbor_buckets(self, n=0):
        # TODO ugly!! refactor
        # n number of buckets to probe
        n_tables = self.dataset.config.stages
        neighbors_in_all_stages = {}

        for bucket, hash_table in zip(
            self.buckets, self.dataset.hash_prober[:n_tables]
        ):
            neighbors = BucketSet()
            neighbors_ = bucket.closest_buckets(n=n, hash_table=hash_table)
            for neighbor in neighbors_:
                neighbors[neighbor.address] = neighbor
            neighbors_in_all_stages.update(neighbors)
        return neighbors_in_all_stages

    def neighbor_points(self):
        # TODO ugly!! refactor
        n_tables = self.dataset.config.stages
        n = ceil(self.t / n_tables)
        neighbor_buckets = self._neighbor_buckets(n)
        neighbor_points = [
            neighbor.points for address, neighbor in neighbor_buckets.items()
        ]
        neighbor_points = list(set(chain.from_iterable(neighbor_points)))
        return neighbor_points

    def get_n_closest_points(self, n=None):
        """Returns n points from (T) probed buckets
        Returns all points in buckets if n is not set.
        """

        if not n:
            return self.neighbor_points()
        else:
            neighbors = self.neighbor_points()
            distances = [self.cosine_similarity(point) for point in neighbors]
            closest_points = sorted(
                zip(distances, neighbors), key=itemgetter(0), reverse=True
            )[1 : n + 1]
            closest_points = [x[1] for x in closest_points]
            return closest_points

    def cosine_similarity(self, other):
        dot_product = np.dot(self.features, other.features)
        norm_a = np.linalg.norm(self.features)
        norm_b = np.linalg.norm(other.features)
        return dot_product / (norm_a * norm_b)

    @property
    def t(self):
        return self.dataset.hash_prober.t

    def one_vs_rest(self, label):
        """Return 1 if the point is in the given label else 0 """
        return self.label == label

    def __str__(self):
        point_str = f"Point index: {self.index}\nPoint buckets:\n"

        for i, bucket in enumerate(self.buckets):
            point_str += f"Stage {i+1}\n"
            point_str += f"{bucket}\n"
            neighbors = self.neighbor_buckets()
            point_str += (
                f"Neighboring buckets to point: {[bucket for bucket in neighbors[i]]}\n"
            )
        return point_str

    def __repr__(self):
        return f"Point with label {self.label} at {self.index}"

    def __getitem__(self, attribute):
        return self.__dict__[attribute]
