import os
import networkx as nx 

# polblogs
# add "multigraph 1" to polblogs.gml in advance.
if not os.path.exists('polblogs/giant_component.gml'):
    g = nx.read_gml('polblogs/polblogs.gml', label='id')
    g = g.to_undirected()
    components = nx.connected_components(g)
    giant_component = nx.Graph(g.subgraph(max(components, key=len)))
    nx.write_gml(giant_component, 'polblogs/giant_component.gml')

# polbooks
if not os.path.exists('polbooks/giant_component.gml'):
    g = nx.read_gml('polbooks/polbooks.gml', label='id')
    mapping = dict(l=0, n=1, c=2)
    for n in g:
        g.nodes[n]['value'] = mapping[g.nodes[n]['value']]
    components = nx.connected_components(g)
    giant_component = nx.Graph(g.subgraph(max(components, key=len)))
    nx.write_gml(giant_component, 'polbooks/giant_component.gml')

# cora
if not os.path.exists('cora/giant_component.gml'):
    g = nx.Graph()
    vertices = []
    with open('cora/cora.node_labels', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            vertex, label =  line.split(',')
            vertices.append((int(vertex)-1, {'value': int(label)}))
    g.add_nodes_from(vertices)

    edges = []
    with open('cora/cora.edges', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            m, n, _ = line.split(',')
            edges.append((int(m)-1, int(n)-1))
    g.add_edges_from(edges)

    components = nx.connected_components(g)
    giant_component = nx.Graph(g.subgraph(max(components, key=len)))
    nx.write_gml(giant_component, 'cora/giant_component.gml')

# citeseer
if not os.path.exists('citeseer/giant_component.gml'):
    g = nx.Graph()
    vertices = []
    with open('citeseer/citeseer.node_labels', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            vertex, label =  line.split(',')
            vertices.append((int(vertex)-1, {'value': int(label)}))
    g.add_nodes_from(vertices)

    edges = []
    with open('citeseer/citeseer.edges', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            m, n, _ = line.split(',')
            edges.append((int(m)-1, int(n)-1))
    g.add_edges_from(edges)

    components = nx.connected_components(g)
    giant_component = nx.Graph(g.subgraph(max(components, key=len)))
    nx.write_gml(giant_component, 'citeseer/giant_component.gml')