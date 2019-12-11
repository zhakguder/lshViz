from py4j.java_gateway import JavaGateway, GatewayParameters
import numpy as np
from math import log, ceil
from sklearn import svm
from util import one_vs_all_partition
from ipdb import set_trace


def get_hashes(feature_lists, stages):

    # buckets = ceil(log(len(feature_lists), 2))
    buckets = len(feature_lists)
    gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
    hashing_app = gateway.entry_point

    value = hashing_app.hash(stages, buckets, feature_lists)
    return value


def get_svm_hyperplanes(feature_lists, *args, **kwargs):
    if not kwargs["labels"]:
        raise TypeError("Need 3 arguments. Pass labels as keyword argument.")

    labels = kwargs["labels"]
    clf = svm.SVC(kernel="linear", C=1000)
    clf.fit(feature_lists, labels)


if __name__ == "__main__":
    from mnist_reader import MnistReader
    from dataset import Dataset

    ds = Dataset(MnistReader)
    # TODO
    # get first 1000 elements and do svm
    get_svm_hyperplanes(ds.features, labels=ds.one_vs_rest_labels(0))
