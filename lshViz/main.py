from mnist_reader import MnistReader
from hashing import get_hashes
from hashDataset import HashDataset
from bucket import BucketSet
from config import LshConfig
from hash_probe import HashProbe
from ipdb import set_trace
from neighborhood_graph import NeighborhoodGraph
from sklearn import svm
from sklearn.model_selection import cross_val_score, StratifiedShuffleSplit
from operator import itemgetter

PER_LABEL_DATASET_SIZE = 10

# LSH settings
STAGES = 10
T = 50

# node2vec settings
WINDOW = 8
NUM_WALKS = 10
WALK_LENGTH = 20
DIM = 15


if __name__ == "__main__":
    import pickle

    ds = HashDataset(
        MnistReader,
        # t=30,
        # stages=10,
        per_label_dataset_size=PER_LABEL_DATASET_SIZE,
    )
    set_trace()
    if "_config" not in ds.__dict__:

        mnistLshConfig = LshConfig(stages=STAGES, t=T)
        mnistLshConfig.per_label_dataset_size = PER_LABEL_DATASET_SIZE
        ds.config = mnistLshConfig

    if ds.hash_prober is None:
        hp = HashProbe(ds.config.t)
        ds.hash_prober = hp
        ds.config.dataset = ds
        # mnistLshConfig.dataset_size = 1000

        for stage in range(ds.config.stages):  # For each stage
            bs = BucketSet()
            bs.attach(hp)  # attach the lsh probing observer
            ds.attach(bs)  # a different bucketset is updated with new buckets
            for observer in bs.observers:
                observer.update(bs)
        ds.populate_buckets()

        mnistLshConfig()

        with open("hashed_" + ds.config.pickle_name, "wb") as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(ds, f, pickle.HIGHEST_PROTOCOL)
    else:
        if ds.embeddings is None:

            neighbor_graph = NeighborhoodGraph(
                edge_file="../node2vec/graph/edges",
                node_label_file="../node2vec/graph/labels",
            )
            neighbor_graph.dataset = ds
            neighbor_graph.populate_graph()
            neighbor_graph.save_graph_info()
            neighbor_graph.get_node2vec_embedding(
                window=WINDOW,
                num_walks=NUM_WALKS,
                walk_length=WALK_LENGTH,
                dim=DIM,
                iter=1,
            )
            with open("embedded_" + ds.config.pickle_name, "wb") as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(ds, f, pickle.HIGHEST_PROTOCOL)
        else:
            set_trace()
        """
        clf = svm.SVC(kernel="linear", C=1000)
        clf.fit(ds.embeddings, ds.labels)
        # scores = cross_val_score(clf, ds.embeddings, ds.labels, cv=5)
        # print(scores)

        # ds.get_tsne_embeddings(2)
        # ds.plot_embeddings("raw_tsne")
        # ds.plot_embeddings("embedding")
        # ds.plot_embeddings("walk_tsne")
        # ds.walk_labels("/tmp/walks.text")
        # classification_attr = "embeddings"
        classification_attr = "embeddings"
        sss = StratifiedShuffleSplit(n_splits=2, test_size=0.5)
        for train_index, test_index in sss.split(ds.embeddings, ds.labels):
            test_features = itemgetter(*test_index)(ds.__dict__[classification_attr])
            test_labels = itemgetter(*test_index)(ds.labels)

            train_features = itemgetter(*train_index)(ds.__dict__[classification_attr])
            train_labels = itemgetter(*train_index)(ds.labels)
            clf.fit(train_features, train_labels)
            acc = 0
            for point, lab in zip(test_features, test_labels):
                if clf.predict(point.reshape(1, -1)) == lab:
                    acc += 1

            print(f"Accuracy: {acc / len(test_labels)}")
            # features = []
            # ds.classify_points(classification_attr, 2)
            # print(ds[test_index])

        # acc = 0
        # for point in ds:
        # point.classification_attribute = classification_attr
        # if clf.predict(point.embeddings.reshape(1, -1)) == point.label:
        # acc += 1

        # print(f"Accuracy: {acc / len(ds)}")

        # # for i in range(10):

        # diameter = ds.hash_prober.diameter(i)
        # print(f"Diameters in all stages for label {i}: {diameter}")
        # for i in range(1, 11):

        #     s = 0
        #     for d in ds:
        #         s += d.get_n_closest_points(i)
        #     print(f"datasize: {ds.config.dataset_size}")
        #     print(f"s: {s}")
"""
