from collections import namedtuple
from math import log, ceil
from hashing import get_hashes
from datetime import datetime
from serialize import PickleNames
from ipdb import set_trace


class LshConfig:
    def __init__(
        self,
        per_label_dataset_size=None,
        stages=1,
        hashing_function="get_hashes",
        dataset_name="mnist",
        t=1,
        config=None,
    ):

        if config:

            self.__dict__ = config
        else:

            self._per_label_dataset_size = per_label_dataset_size
            self.stages = stages
            self._hashing_function = hashing_function

            self.dataset_name = dataset_name
            self.start_time = str(datetime.now())
            self._t = t
            self._pickle_name = None
        self._dataset = None

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t = t

    @property
    def code_length(self):
        return ceil(log(self.per_label_dataset_size, 2))

    @property
    def per_label_dataset_size(self):
        if self._per_label_dataset_size:
            return self._per_label_dataset_size
        else:
            return len(self.dataset.points)

    @per_label_dataset_size.setter
    def per_label_dataset_size(self, per_label_dataset_size):
        self._per_label_dataset_size = per_label_dataset_size

        # self.pickle_names = PickleNames(self.pickle_name)

    @property
    def pickle_name(self):
        return self._pickle_name

    @pickle_name.setter
    def pickle_name(self, name):
        self._pickle_name = name

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        # e.g. HashDataset
        dataset.config = self
        self._dataset = dataset

    @property
    def hashing_function(self):
        return eval(self._hashing_function)

    @hashing_function.setter
    def hashing_function(self, hashing_function):
        self._hashing_function = hashing_function

    def __call__(self):
        import json

        try:
            with open("config.json") as f:
                config_data = json.load(f)
                cnt = max([int(c) for c in config_data.keys()]) + 1
        except:
            cnt = 1
            config_data = {}

        self.number = cnt
        self.pickle_name = f"{self.dataset_name}_{self.per_label_dataset_size}_{self.number}.pickle".replace(
            " ", "_"
        )
        state = self.__dict__.copy()
        del state["_dataset"]

        config_data.update({cnt: state})
        with open("config.json", "w") as f:
            json.dump(config_data, f)


if __name__ == "__main__":
    from mnist_reader import MnistReader
    from hashing import get_hashes
    from hashDataset import HashDataset
    from bucket import BucketSet
    from config import LshConfig

    mnistLshConfig = LshConfig(stages=2)
    ds = HashDataset(MnistReader)
    mnistLshConfig.dataset = ds
    mnistLshConfig.per_label_dataset_size = 10

    ds.config = mnistLshConfig
    for stage in range(ds.stages):  # For each stage
        ds.attach(BucketSet())  # a different bucketset is updated with new buckets
    ds.populate_buckets()

    mnistLshConfig()

    print(ds)
    for d in ds:
        print(d)
