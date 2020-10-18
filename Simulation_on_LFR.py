import pickle
import igraph as ig
import networkx as nx
from FPPM import FPPM_repeat
from igraph.clustering import compare_communities

DIR_FMT = 'LFR_benchmarks/N{}/'
GML_FMT = 'Mu{}-{}.gml'
SIZES = [250, 500, 1000]

Fastgreedy_performance = [[], [], []]
Infomap_performance = [[], [], []]
LPA_performance = [[], [], []]
Louvein_performance = [[], [], []]
Walktrap_performance = [[], [], []]
FPPM_performance = [[], [], []]

for idx, N in enumerate(SIZES):
    for Mu in range(1, 10):
        for _ in range(100):
            file = DIR_FMT.format(N) + GML_FMT.format(Mu, _)
            g = ig.Graph.Read_GML(file)
            ground_truth = [int(v['value']) for v in g.vs]

            for __ in range(100):
                p1 = g.community_fastgreedy().as_clustering()
                p2 = g.community_infomap()
                p3 = g.community_label_propagation()
                p4 = g.community_multilevel()
                p5 = g.community_walktrap().as_clustering()

                Fastgreedy_performance[idx].append(compare_communities(ground_truth, p1, method='nmi'))
                Infomap_performance[idx].append(compare_communities(ground_truth, p2, method='nmi'))
                LPA_performance[idx].append(compare_communities(ground_truth, p3, method='nmi'))
                Louvein_performance[idx].append(compare_communities(ground_truth, p4, method='nmi'))
                Walktrap_performance[idx].append(compare_communities(ground_truth, p5, method='nmi'))

            g = nx.read_gml(file, label='id')
            partitions = FPPM_repeat(g)
            for p in partitions:
                FPPM_performance[idx].append(compare_communities(ground_truth, p, method='nmi'))

with open('LFR_benchmarks/Fastgreedy_performance.pickle', 'wb') as f:
    pickle.dump(Fastgreedy_performance, f)
with open('LFR_benchmarks/Infomap_performance.pickle', 'wb') as f:
    pickle.dump(Infomap_performance, f)
with open('LFR_benchmarks/LPA_performance.pickle', 'wb') as f:
    pickle.dump(LPA_performance, f)
with open('LFR_benchmarks/Louvein_performance.pickle', 'wb') as f:
    pickle.dump(Louvein_performance, f)
with open('LFR_benchmarks/Walktrap_performance.pickle', 'wb') as f:
    pickle.dump(Walktrap_performance, f)
with open('LFR_benchmarks/FPPM_performance.pickle', 'wb') as f:
    pickle.dump(FPPM_performance, f)
