import pickle
import igraph as ig
import networkx as nx
from FPPM import FPPM_repeat
from igraph.clustering import compare_communities

DIR_FMT = 'Planted_LPartition_benchmarks/N{}/'
GML_FMT = 'din{}-{}.gml'

Fastgreedy_performance = [[], []]
Infomap_performance = [[], []]
LPA_performance = [[], []]
Louvein_performance = [[], []]
Walktrap_performance = [[], []]
FPPM_performance = [[], []]

# first parameter group
for din in range(9, 18):
    for _ in range(10):
        file = DIR_FMT.format(64) + GML_FMT.format(din, _)
        g = ig.Graph.Read_GML(file)
        ground_truth = [int(v['value']) for v in g.vs]

        for __ in range(100):
            p1 = g.community_fastgreedy().as_clustering()
            p2 = g.community_infomap()
            p3 = g.community_label_propagation()
            p4 = g.community_multilevel()
            p5 = g.community_walktrap().as_clustering()
            
            Fastgreedy_performance[0].append(compare_communities(ground_truth, p1, method='nmi'))
            Infomap_performance[0].append(compare_communities(ground_truth, p2, method='nmi'))
            LPA_performance[0].append(compare_communities(ground_truth, p3, method='nmi'))
            Louvein_performance[0].append(compare_communities(ground_truth, p4, method='nmi'))
            Walktrap_performance[0].append(compare_communities(ground_truth, p5, method='nmi'))

        g = nx.read_gml(file, label='id')
        partitions = FPPM_repeat(g)
        for p in partitions:
            FPPM_performance[0].append(compare_communities(ground_truth, p, method='nmi'))

# second parameter group
for din in range(4, 16):
    for _ in range(10):
        file = DIR_FMT.format(128) + GML_FMT.format(din, _)
        g = ig.Graph.Read_GML(file)
        ground_truth = [int(v['value']) for v in g.vs]

        for __ in range(100):
            p1 = g.community_fastgreedy().as_clustering()
            p2 = g.community_infomap()
            p3 = g.community_label_propagation()
            p4 = g.community_multilevel()
            p5 = g.community_walktrap().as_clustering()

            Fastgreedy_performance[1].append(compare_communities(ground_truth, p1, method='nmi'))
            Infomap_performance[1].append(compare_communities(ground_truth, p2, method='nmi'))
            LPA_performance[1].append(compare_communities(ground_truth, p3, method='nmi'))
            Louvein_performance[1].append(compare_communities(ground_truth, p4, method='nmi'))
            Walktrap_performance[1].append(compare_communities(ground_truth, p5, method='nmi'))
        
        g = nx.read_gml(file, label='id')
        partitions = FPPM_repeat(g)
        for p in partitions:
            FPPM_performance[1].append(compare_communities(ground_truth, p, method='nmi'))

with open('Planted_LPartition_benchmarks/Fastgreedy_performance.pickle', 'wb') as f:
    pickle.dump(Fastgreedy_performance, f)
with open('Planted_LPartition_benchmarks/Infomap_performance.pickle', 'wb') as f:
    pickle.dump(Infomap_performance, f)
with open('Planted_LPartition_benchmarks/LPA_performance.pickle', 'wb') as f:
    pickle.dump(LPA_performance, f)
with open('Planted_LPartition_benchmarks/Louvein_performance.pickle', 'wb') as f:
    pickle.dump(Louvein_performance, f)
with open('Planted_LPartition_benchmarks/Walktrap_performance.pickle', 'wb') as f:
    pickle.dump(Walktrap_performance, f)
with open('Planted_LPartition_benchmarks/FPPM_performance.pickle', 'wb') as f:
    pickle.dump(FPPM_performance, f)