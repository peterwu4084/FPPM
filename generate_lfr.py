# LFR Program can be downloaded from
# https://sites.google.com/site/santofortunato/benchmark.tgz

import os
import networkx as nx 

BENCHMARK = 'benchmark -N {} -k {} -maxk {} -mu {:.2f} -t1 {} -t2 {} -minc {} -maxc {}'
GML_FMT = 'Mu{}-{}.gml'
DIR_FMT = 'LFR_benchmarks/N{}/'
K = 25
MAXK = 50
T1 = 2
T2 = 1
MINC = 20
MAXC = 50

def dat2gml(network_dat, community_dat, gml_file):
    '''
    Convert .dat produced by benchmark to .gml.

    Parameters
    ----------
    network_dat : str
        The path to the network.dat.
    community_dat : str
        The path to the community.dat.
    gml_file : str
        The path to save .gml file.

    Returns
    -------
    return : None
    '''
    g = nx.Graph()
    with open(network_dat) as f:
        for line in f.readlines():
            line = line.strip()
            m, n = line.split('\t')
            g.add_edge(int(m)-1, int(n)-1)
    with open(community_dat) as f:
        for line in f.readlines():
            line = line.strip()
            vertex, club = line.split('\t')
            g.nodes[int(vertex)-1]['value'] = int(club)
    nx.write_gml(g, gml_file)

def generate(N, k, maxk, t1, t2, minc, maxc):
    '''
    Generate LFR benchmarks and save as .gml files.
    The mixing parameter traverses {0.1, 0.2, ..., 0.9}.
    For each combination of parameters, 10 networks are produced.

    Parameters
    ----------
    N : int
        The size of the generate.
    k : int
        The average of degrees.
    maxk : int
        The maximal degree.
    t1 : float
        The exponent of the distribution of community size.
    t2 : float
        The exponent of the distribution of degree.
    minc : int
        The minimal size of communities.
    maxc : int
        The maximal size of communities.

    Returns
    -------
    return : None
    '''
    for mu in range(1, 10):
        for _ in range(100):
            os.system(BENCHMARK.format(N, k, maxk, mu/10, t1, t2, minc, maxc))
            gml_file = DIR_FMT.format(N) + GML_FMT.format(mu, _)
            dat2gml('network.dat', 'community.dat', gml_file)

if __name__ == '__main__':
    if not os.path.exists('LFR_benchmarks'):
        os.mkdir('LFR_benchmarks')
        os.mkdir('LFR_benchmarks/N1000')
        os.mkdir('LFR_benchmarks/N500')
        os.mkdir('LFR_benchmarks/N250')

    for N in [250, 500, 1000]:
        with open('time_seed.dat', 'w') as f:
            f.write('21113333')
        generate(N, K, MAXK, T1, T2, MINC, MAXC)

    os.system('del *.dat')
