import pickle
import igraph as ig
import networkx as nx
from FPPM import FPPM_repeat
from igraph.clustering import compare_communities

Fastgreedy_performance = [[], [], [], []]
Infomap_performance = [[], [], [], []]
LPA_performance = [[], [], [], []]
Louvein_performance = [[], [], [], []]
Walktrap_performance = [[], [], [], []]
FPPM_performance = [[], [], [], []]

networks = [
    ig.Graph.Read_GML('Real_Networks/polblogs/giant_component.gml'),
    ig.Graph.Read_GML('Real_Networks/polbooks/giant_component.gml'),
    ig.Graph.Read_GML('Real_Networks/cora/giant_component.gml'),
    ig.Graph.Read_GML('Real_Networks/citeseer/giant_component.gml'),
]
ground_truths = [
    [int(v['value']) for v in g.vs] for g in networks
]
for idx, g in enumerate(networks):
    for _ in range(100):
        p1 = g.community_fastgreedy().as_clustering()
        p2 = g.community_infomap()
        p3 = g.community_label_propagation()
        p4 = g.community_multilevel()
        p5 = g.community_walktrap().as_clustering()

        Fastgreedy_performance[idx].append(compare_communities(ground_truths[idx], p1, method='nmi'))
        Infomap_performance[idx].append(compare_communities(ground_truths[idx], p2, method='nmi'))
        LPA_performance[idx].append(compare_communities(ground_truths[idx], p3, method='nmi'))
        Louvein_performance[idx].append(compare_communities(ground_truths[idx], p4, method='nmi'))
        Walktrap_performance[idx].append(compare_communities(ground_truths[idx], p5, method='nmi'))

networks = [
    nx.read_gml('Real_Networks/polblogs/giant_component.gml', label='id'),
    nx.read_gml('Real_Networks/polbooks/giant_component.gml', label='id'),
    nx.read_gml('Real_Networks/cora/giant_component.gml', label='id'),
    nx.read_gml('Real_Networks/citeseer/giant_component.gml', label='id'),
]
for idx, g in enumerate(networks):
    partitions = FPPM_repeat(g)
    for p in partitions:
        FPPM_performance[idx].append(compare_communities(ground_truths[idx], p, method='nmi'))

with open('Real_Networks/Fastgreedy_performance.pickle', 'wb') as f:
    pickle.dump(Fastgreedy_performance, f)
with open('Real_Networks/Infomap_performance.pickle', 'wb') as f:
    pickle.dump(Infomap_performance, f)
with open('Real_Networks/LPA_performance.pickle', 'wb') as f:
    pickle.dump(LPA_performance, f)
with open('Real_Networks/Louvein_performance.pickle', 'wb') as f:
    pickle.dump(Louvein_performance, f)
with open('Real_Networks/Walktrap_performance.pickle', 'wb') as f:
    pickle.dump(Walktrap_performance, f)
with open('Real_Networks/FPPM_performance.pickle', 'wb') as f:
    pickle.dump(FPPM_performance, f)