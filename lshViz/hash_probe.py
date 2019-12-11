from ipdb import set_trace
from itertools import combinations
from util import hamming


class HashProbe:
    def __init__(self, t):
        """K, the number of hash functions (space partitions) per hash table.

        L, the number of hash tables (each of which has K hash
        functions).

        T, the number of probes (total number of buckets
        probed across all hash tables).

        The higher the K, the higher the L should be. Too costly, but
        one can probe more than one bucket in each table. T is the
        total number of probed buckets over all tables.
        """
        # self.k = k # TODO: refactor and add here as param
        # self.l = l # TODO: refactor and add here as param
        self._t = t
        self._hash_tables = []

    def diameter(self, label):
        max_dists = []
        for table in self:

            buckets_containing_label = [
                bucket
                for bucket in self[0].values()
                if any(map(lambda x: x.filter_label(label), bucket.points))
            ]
            max_dist = 0
            for pair in combinations(buckets_containing_label, 2):

                dist = hamming(*map(lambda x: x.address, pair))

                if dist > max_dist:
                    max_dist = dist
            max_dists.append(max_dist)
        return max_dists

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t = t

    @property
    def hash_tables(self):
        return self._hash_tables

    @hash_tables.setter
    def hash_tables(self, hash_table):
        self._hash_tables.append(hash_table)

    def update(self, hash_table):
        self.hash_tables = hash_table

    def __getitem__(self, i):
        return self.hash_tables[i]

    def __iter__(self):
        return self.hash_tables.__iter__()

    def __len__(self):
        return self.hash_tables.__len__()

    def __str__(self):
        hp_str = "HASH TABLES\n"

        for i, table in enumerate(self):
            hp_str += f"Table {i}:\n{table}\n"
        return hp_str
