import numpy as np
import networkx as nx
from copy import deepcopy
from collections import defaultdict, deque
from scipy.cluster.hierarchy import average, to_tree

def diag_matrix(X):
    '''
    Get the diagonal matrix of X.

    Parameters
    ----------
    X : 2d numpy.ndarray
        A matrix.
    
    Returns
    -------
    return : 2d numpy.ndarray
        The diagonal matrix of the input matrix.
    '''
    return np.diag(np.diag(X))

def normalize(X):
    '''
    Translate X to Y where Y[i, j] = X[i, j] / sum(X[i, :]).
    The sum of any row of X can't be 0.

    Parameters
    ----------
    X : 2d numpy.ndarray
        The input matrix.

    Returns
    -------
    return : 2d numpy.ndarray
        The normalised matrix that the sum of any row is 1.
    '''
    row_sum = X.sum(axis=1).reshape(-1, 1)
    return X / row_sum

def transition_matrix(G):
    '''
    TODO

    Parameters
    ----------
    G : networkx.Graph
        A graph.

    Returns
    -------
    T : 2d numpy.ndarray
        The transition matrix.
    '''
    T = []
    for n in G:
        row = []
        nbrs_n = set(G.neighbors(n))
        for m in G:
            if m in nbrs_n:
                nbrs_m = set(G.neighbors(m))
                common_nbr = len(nbrs_n.intersection(nbrs_m)) + 1
                row.append(common_nbr)
            else:
                row.append(0)
        T.append(row)
    return normalize(np.array(T))

def first_passage_prob(T, n):
    '''
    Calculate and yield the i-step first passage probabilities.
    i is smaller than or equal to n.

    Parameters
    ----------
    T : 2d numpy.ndarray
        The transition matrix.
    n : int
        The number of steps
    '''
    F = T.copy()
    yield F
    for _ in range(1, n):
        F = T.dot(F - diag_matrix(F))
        yield F

def hierarchical_clustering(similarity):
    '''
    Yield partitions by hierarchical clustering with average similarity.
    
    Parameters
    ----------
    similarity : 2d numpy.ndarray
        The similarity matrix.
    '''
    # m, _ = similarity.shape
    # communities = [{i} for i in range(m)]
    # similarity = similarity - diag_matrix(similarity)
    # yield communities
    # while len(communities) > 2:
    #     max_idx = np.argmax(similarity)
    #     max_idx = np.unravel_index(max_idx, similarity.shape)
    #     i, j = min(max_idx), max(max_idx)

    #     similarity = np.delete(similarity, j, axis=1)
    #     similarity = np.delete(similarity, i, axis=1)
    #     ri = similarity[i, :]
    #     rj = similarity[j, :]
    #     similarity = np.delete(similarity, j, axis=0)
    #     similarity = np.delete(similarity, i, axis=0)        

    #     cj = communities.pop(j)
    #     ci = communities.pop(i)
    #     communities.append(ci.union(cj))
    #     li, lj = len(ci), len(cj)
    #     rn = (li * ri + lj * rj) / (li + lj)
    #     similarity = np.vstack((similarity, rn))
    #     rn = np.concatenate((rn, [0])).reshape(-1, 1)
    #     similarity = np.hstack((similarity, rn))
    #     yield communities
    m, _ = similarity.shape
    similarity = np.array([similarity[i, j] for i in range(m) for j in range(i+1, m)])
    distance = 1 - similarity
    dendrogram = average(distance)
    _, nodelist = to_tree(dendrogram, rd=True)
    id2vertices = {i:{i} for i in range(m)}
    yield id2vertices.values()
    for _ in range(m, 2 * m - 1):
        node = nodelist[_]
        left = node.left.id
        right = node.right.id
        new_community = id2vertices[left].union(id2vertices[right])
        id2vertices[node.id] = new_community
        del id2vertices[left]
        del id2vertices[right]
        yield id2vertices.values()

def select_by_Q(dendrogram, G):
    '''
    Select the partition with the maximal modularity from the dendrogram.

    Parameters
    ----------
    dendrogram : generator
        A generator of partitions from fine to coarse.
    G : networkx.Graph
        A graph.

    Returns
    -------
    return : list
        A community partition.
    '''
    best = None
    maxQ = -1
    for partition in dendrogram:
        Q = nx.community.modularity(G, partition)
        if Q > maxQ:
            maxQ = Q
            best = [_ for _ in partition]
    return best

def remove_small_communities(partition, G, S, theta):
    '''
    Merge small communities into big communities.
    Parameters
    ----------
    partition : set
        A set of communities.
    G : networkx.Graph
        A graph.
    S : 2d numpy.ndarray
        The similarity matrix.
    theta : int
        The minimal size of communities.

    Returns
    -------
    return : list
        The ith element is the label of vertex i.
    '''
    labels = {}
    for idx, community in enumerate(partition):
        for vertex in community:
            labels[vertex] = idx

    small_communities = deque()
    large_labels = set()
    for community in partition:
        if len(community) >= theta:
            some_vertex = next(iter(community))
            large_labels.add(labels[some_vertex])
        else:
            small_communities.append(community)
    while small_communities:
        community = small_communities.popleft()
        relevance = defaultdict(lambda: 0)
        for v in community:
            for _ in G.neighbors(v):
                if _ not in community and labels[_] in large_labels:
                    relevance[labels[_]] += S[v, _]
        if relevance:
            mergeto = max(relevance, key=relevance.get)
            for v in community:
                labels[v] = mergeto
        else:
            small_communities.append(community)
    return [labels[_] for _ in range(len(G))]

def FPPM(G, theta=3):
    '''
    FPPM to detect communities.

    Parameters
    ----------
    G : networkx.Graph
        A graph
    theta : int, optional
        The minimal size of communities.

    Returns
    -------
    return : list
        The ith element is the label of vertex i.
    '''
    d = nx.diameter(G)
    if d <= 3:
        ds = {2}
    else:
        ds = set(range(2, d))
    T = transition_matrix(G)
    S = np.zeros(T.shape)
    for idx, F in enumerate(first_passage_prob(T, max(ds)+1)):
        S += np.corrcoef(F)
    S /= len(ds)
    dendrogram = hierarchical_clustering(S)
    partition_Q = select_by_Q(dendrogram, G)
    partition = remove_small_communities(partition_Q, G, S, theta)
    return partition

def FPPM_repeat(G, theta=3, repeat=100):
    '''
    FPPM to detect communities with repeat. Because the calculation of 
    vertex similarities, hierarchical clustering and selecting th partition
    with the maximal modularity from the dendrogram are fixed and the final
    partition can be influenced by the ordering of small communities in the 
    processing of removing small communities. Only removig small communities
    are repeated.

    Parameters
    ----------
    G : networkx.Graph
        A graph
    theta : int, optional
        The minimal size of communities, default to be 3.
    repeat : int, option
        The repeat times, default to be 100.

    Returns
    -------
    return : list
        The ith element is the label of vertex i.
    '''
    d = nx.diameter(G)
    if d <= 3:
        ds = {2}
    else:
        ds = set(range(2, d))
    T = transition_matrix(G)
    S = np.zeros(T.shape)
    for idx, F in enumerate(first_passage_prob(T, max(ds)+1)):
        S += np.corrcoef(F)
    S /= len(ds)
    dendrogram = hierarchical_clustering(S)
    partition_Q = select_by_Q(dendrogram, G)
    partitions = []
    for _ in range(repeat):
        partitions.append(remove_small_communities(partition_Q, G, S, theta))
    return partitions

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    G = nx.karate_club_graph()
    partition = FPPM(G)
    nx.draw(G, node_color=partition, with_labels=True)
    plt.show()
