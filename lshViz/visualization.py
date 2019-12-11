from sklearn.manifold import TSNE


def tsne(x, n_components):
    """Returns n_components dimensional embeddings for x

    Args:
       x (np.ndarray): Input vector to be embedded. Rows are examples, columns are features.
       n_components (int): Embedding dimension.

    Returns:
       np.ndarray. Embeddings"""

    embeddings = TSNE(n_components=n_components).fit_transform(x)
    return embeddings
