from random import shuffle
from ipdb import set_trace
from util import get_combinations


class Bucket:
    def __init__(self, address):

        self.address = address
        self._points = []

    def add_point(self, point):
        self._points.append(point)

    def closest_buckets(self, n=0, hash_table=None):  # TODO
        """Returns n many closest buckets"""
        neighbors = [hash_table[self.address]]
        # Look in buckets increasing in hamming distance

        bit_positions_at_distance = get_combinations(range(Bucket.code_length))

        i = 0
        cont = True
        while cont:
            i += 1
            bit_position_permutations = bit_positions_at_distance(
                i
            )  # get bit positions to flip at Hamming  distance i

            for bit_pos in bit_position_permutations:
                if n == 0:
                    cont = False
                    break
                n -= 1  # decrease number of buckets to be probed
                neighbor = self.address
                for k in bit_pos:
                    neighbor = neighbor ^ (1 << k)
                if neighbor in hash_table:
                    neighbors.append(hash_table[neighbor])
        return neighbors

    @property
    def points(self):
        return self._points

    def __lt__(self, other):
        return self.address < other.address

    # @property
    # def bit_address(self):
    #     return f"{self.address:b}".zfill(lsh_config.code_length)

    def __repr__(self):
        return f"{self}"

    def __str__(self):
        points = sorted(self.points)
        res_str = f"Bucket {self.address}:\n\tIndices: {[j.index for j in points]}\n\tLabels: {[j.label for j in points]}\n"
        return res_str


class BucketSet(dict):
    def __init__(self):
        super().__init__()
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def update(self, bucket):
        if bucket in self:
            b = self[bucket]
        else:
            b = Bucket(bucket)
            self[bucket] = b
        return b

    def __lt__(self, other):
        return self.address < other.address

    def __str__(self):
        bucket_str = ""

        for k, v in sorted(self.items()):
            bucket_str += f"{v}"

        return bucket_str
