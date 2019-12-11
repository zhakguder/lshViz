from itertools import combinations
from collections import Counter
from ipdb import set_trace


def get_combinations(lst):
    """Yields one permutation with increasing number of elements from the list"""

    def permute(i):
        yield from combinations(lst, i)

    return permute


def hamming(x, y):
    diff = x ^ y
    return Counter(bin(diff))["1"]


def one_vs_all(y, query_label):

    """Given labels y and the class to be compared with rest, returns a
    list with 1 if the example is of the class to be compared and 0 otherwise"""

    labels = []

    labels = [int(label == query_label) for label in y]

    return labels


def one_vs_all_partition(y):
    """Given a list of labels, returns a dictionary where each key is a
    class and each value is a list with 1/0's indicating membership in
    the class to be compared against.
    """
    max_label = max(y)

    one_vs_all_labels = {}
    for query_label in range(max_label + 1):
        one_vs_all_labels[query_label] = one_vs_all(y, query_label)
    return one_vs_all_labels


def filter_labels(y, query_label):
    return [i for i, x in enumerate(y) if x == query_label]


def sample_random_indices_of_per_label_size(number_of_options, n):
    """n: how many points per label"""
    import random

    return random.sample(range(number_of_options), n)


def get_n_points_per_label(y, query_label, n):
    can_keep = filter_labels(y, query_label)
    index_indices = sample_random_indices_of_per_label_size(len(can_keep), n)
    return [can_keep[ind_ind] for ind_ind in index_indices]


def get_sized_random_subset(y, n):
    min_ = int(min(y))
    max_ = int(max(y))

    keep_indices = []

    for query_label in range(min_, max_ + 1):
        indices = get_n_points_per_label(y, query_label, n)
        keep_indices.extend(indices)
    return keep_indices


if __name__ == "__main__":
    from dataset import Dataset
    from mnist_reader import MnistReader

    ds = Dataset(MnistReader, 10)
