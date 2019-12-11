import os
import json
import sys
import matplotlib.pyplot as plt
from itertools import combinations
from ipdb import set_trace

FIG_NO = 0


def read_node2vec_emb(fname):
    with open(fname, "r") as handle:
        content = handle.readlines()

        nodes = []
        xs = []
        ys = []

        for line in content[1:]:
            node_id, x, y = line.strip().split(" ")

            x = float(x)
            y = float(y)
            xs.append(x)
            ys.append(y)
            nodes.append(node_id)

        return nodes, xs, ys


def get_labels(fname):
    mapping = {}
    with open(fname, "r") as handle:
        content = handle.readlines()
        for line in content:
            node, label = line.strip().split(",")
            mapping[node] = int(label)

    return mapping


def plot2d(emb, mapping, pair, plot_base_name):
    nodes, xs, ys = read_node2vec_emb(emb)
    mapping = get_labels(mapping)
    colors = {
        1: "tab:blue",
        2: "tab:orange",
        3: "tab:green",
        4: "tab:red",
        5: "tab:purple",
        6: "tab:brown",
        7: "tab:pink",
        8: "tab:gray",
        9: "tab:olive",
        0: "tab:cyan",
    }
    global FIG_NO
    FIG_NO += 1
    plt.figure(FIG_NO)

    for ind, val in enumerate(zip(xs, ys)):
        x, y = val
        label = int(mapping[nodes[ind]])
        # if label in pair:
        plt.scatter(x, y, color=colors[label], label=label)
    # plt.title("{} - {}".format(*pair))
    # fig_name = "minst_{}_{}.png".format(*pair)
    # plot_path = os.path.join(plot_base_name, fig_name)
    # plt.savefig(plot_path)
    # colors = []
    # plt.scatter(xs, ys, color)
    plt.show()


def walk_to_labels(walk_fname, label_fname):
    mapping = get_labels(label_fname)
    with open(walk_fname, "r") as handle:
        walks = handle.readlines()
        for walk in walks:
            walk = walk.replace("[", "").replace("]", "")
            print("WALK")
            print(walk)
            print([mapping[n.strip()] for n in walk.strip().split(",")])


emb_file = sys.argv[1]
mapping_file = sys.argv[2]
plt_base_name = sys.argv[3]
label_pairs = combinations(range(10), 2)
for pair in label_pairs:
    plot2d(emb_file, mapping_file, pair, plt_base_name)
# walk_to_labels(sys.argv[1], sys.argv[2])
