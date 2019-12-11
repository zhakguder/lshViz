import networkx as nx
from ipdb import set_trace
import os
from n2v import node2vec
from n2v.main import learn_embeddings


class NeighborhoodGraph:
    def __init__(self, hash_dataset=None, edge_file=None, node_label_file=None):
        self._dataset = hash_dataset
        self.neighborhood_graph = nx.DiGraph()
        self.edge_file = edge_file
        self.node_label_file = node_label_file

    def populate_graph(self):
        for point in self.dataset:
            node_attr = {point.index: point.label}
            neighbor_list = point.get_n_closest_points(10)
            edges_incident_to_node = []
            for neighbor in neighbor_list:
                edges_incident_to_node += [(point.index, neighbor.index)]
                node_attr.update({neighbor.index: neighbor.label})

            self.neighborhood_graph.add_edges_from(edges_incident_to_node)
            nx.set_node_attributes(self.neighborhood_graph, node_attr, "label")

    def save_graph_info(self):
        os.remove(self.edge_file)
        os.remove(self.node_label_file)
        nx.write_edgelist(self.neighborhood_graph, self.edge_file, data=False)
        mapping = dict(
            [
                (node, int(cls["label"]))
                for node, cls in self.neighborhood_graph.nodes(data=True)
            ]
        )
        for node, label in mapping.items():
            print(f"{node},{label}", file=open(self.node_label_file, "a+"))

    def get_node2vec_embedding(
        self,
        dim=2,
        window=5,
        iter=1,
        num_walks=10,
        walk_length=80,
        embedding_file="/tmp/embed",
    ):
        G = self.neighborhood_graph.copy()
        for edge in G.edges():
            G[edge[0]][edge[1]]["weight"] = 1
        G = node2vec.Graph(G, True, 1, 1)
        G.preprocess_transition_probs()
        walks = G.simulate_walks(num_walks, walk_length)
        print("done generating walks")
        embeddings = learn_embeddings(walks=walks, dim=dim, window=window, iter=iter)
        print("done generating walk embeddings")
        self.dataset.set_node2vec_embeddings(embeddings)

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        self._dataset = dataset


if __name__ == "__main__":
    a = NeighborhoodClass()
