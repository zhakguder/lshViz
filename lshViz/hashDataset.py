import os
from bucket import Bucket
from dataset import Dataset
from data_reader import DataReader
from point import HashPoint
from load import load_hashed_dataset
from ipdb import set_trace


class HashDataset(Dataset):
    def __init__(
        self, data_reader=DataReader, t=None, stages=None, per_label_dataset_size=None
    ):
        """
        Load type should be hashed or embedded or empty
        """
        temp = load_hashed_dataset()
        # temp._embeddings = None

        if temp:
            object().__init__()
            self.__setstate__(temp.__dict__)
            Bucket.code_length = self.config.code_length
            if stages:
                self.config.stages = stages
            if t:
                temp.hash_prober.t = temp.config.t = t
        else:
            super().__init__(data_reader, per_label_dataset_size=per_label_dataset_size)
            self._hashing_function = None
            self._hashes = None
            self.hashed_points = []
            self.observers = []
            self._hash_prober = None
            self._embeddings = None
            HashPoint.dataset = self

    def __getstate__(self):
        state = self.__dict__.copy()
        keys = ["_hashing_function"]  # , "_config"]
        for key in keys:
            if key in state:
                del state[key]

        return state

    def __setstate__(self, state):
        hash_tables = state["_hash_prober"].hash_tables
        for table in hash_tables:
            for key, value in table.items():
                for point in value.points:
                    point._buckets.append(value)
        self.__dict__ = state
        HashPoint.dataset = self

    def attach(self, observer):
        self.observers.append(observer)

    def populate_buckets(self):

        Bucket.code_length = self.config.code_length

        self._process_features()

        for point, bucket in zip(self.points, self._hashes):

            hash_point = HashPoint(point)

            for i, observer in enumerate(self.observers):

                b = observer.update(bucket[i])
                hash_point.buckets = b

            self.hashed_points.append(hash_point)
        del self._hashes
        del self.points
        del self.observers

    def _process_features(self):

        list_features = [x.features.tolist() for x in self.points]

        self.hashes = self.hashing_function(list_features, self.stages)

    def set_node2vec_embeddings(self, embeddings):
        # TODO: play with node2vec parameters in neighborhood_graph from main
        self.embeddings = embeddings
        for point, embedding in zip(self.hashed_points, embeddings):
            point.embeddings = embedding

    def plot_embeddings(self, point_attribute):
        import matplotlib.pyplot as plt
        from plot_settings import label_colors

        labels = [point.label for point in self]
        from collections import Counter

        print(Counter(labels))
        for point in self:
            x, y = point[point_attribute]
            label = point.label
            plt.scatter(x, y, color=label_colors[label], label=label)
        plt.show()

    def walk_labels(self, walk_file):
        mapping = {point.index: point.label for point in self}
        with open(walk_file, "r") as handle:
            walks = handle.readlines()
            for walk in walks:
                walk = walk.strip("\n").replace("['", "").replace("']", "")
                print("WALK")
                print(walk)
                print([mapping[int(n.strip())] for n in walk.strip().split(" ")])
                print()

    def get_tsne_embeddings(self, n_components):
        from visualization import tsne

        raw_embeddings = tsne(self.features, n_components)
        walk_embeddings = tsne(self.embeddings, n_components)
        for point, r_emb, w_emb in zip(
            self.hashed_points, raw_embeddings, walk_embeddings
        ):
            point.raw_tsne = r_emb
            point.walk_tsne = w_emb

    @property
    def hashing_function(self):
        return self.config.hashing_function

    @property
    def stages(self):
        return self.config.stages

    @property
    def hashes(self):
        return self._hashes

    @hashes.setter
    def hashes(self, hashes):
        self._hashes = hashes

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def hash_prober(self):
        return self._hash_prober

    @hash_prober.setter
    def hash_prober(self, hash_prober):
        self._hash_prober = hash_prober

    @property
    def embeddings(self):
        return self._embeddings

    @embeddings.setter
    def embeddings(self, embeddings):
        self._embeddings = embeddings

    def __iter__(self):
        return self.hashed_points.__iter__()

    def __getitem__(self, i):
        return self.hashed_points[i]

    def __str__(self):
        hash_str = ""
        for i, observer in enumerate(self.observers):
            hash_str += f"\nStage {i+1}\n"
            hash_str += "-" * 30 + "\n"
            hash_str += f"{observer}\n"

        hash_str += "-" * 30 + "\n"

        return hash_str

    def __len__(self):
        return len(self.hashed_points)


if __name__ == "__main__":
    from mnist_reader import MnistReader
    from bucket import BucketSet
    from hash_probe import HashProbe

    hp = HashProbe(5)
    ds = HashDataset(MnistReader)
    ds.hash_prober = hp
    ds.hashing_function = get_hashes  # get hashes does superBitLsh
    for stage in range(ds.stages):  # For each stage
        bs = BucketSet()
        bs.attach(hp)  # attach the lsh probing observer
        ds.attach(bs)  # a different bucketset is updated with new buckets
        for observer in bs.observers:
            observer.update(bs)
    ds.populate_buckets()
