import os
import networkx as nx 
from Planted_LPartition import Planted_LPartition

FIRST_PARAMETER_GROUP = dict(l=2, Nc=32)
SECOND_PARAMETER_GROUP = dict(l=4, Nc=32)
DIR_FMT = 'Planted_LPartition_benchmarks/N{}/'
GML_FML = 'din{}-{}.gml'

if __name__ == '__main__':
    if not os.path.exists('Planted_LPartition_benchmarks'):
        os.mkdir('Planted_LPartition_benchmarks')
        os.mkdir('Planted_LPartition_benchmarks/N64')
        os.mkdir('Planted_Lpartition_benchmarks/N128')

    
    for dout in range(1, 10):
        for _ in range(100):
            din = 18 - dout
            g = Planted_LPartition(pin=din/31, pout=dout/32, **FIRST_PARAMETER_GROUP)
            nx.write_gml(g, DIR_FMT.format(64)+GML_FML.format(din, _))

    for din in range(4, 16):
        for _ in range(100):
            dout = 16 - din
            g = Planted_LPartition(pin=din/31, pout=dout/96, **SECOND_PARAMETER_GROUP)
            nx.write_gml(g, DIR_FMT.format(128)+GML_FML.format(din, _))
