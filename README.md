# First Passage Probability Method
This repository contains the codes of FPPM and the simulations in "Community detection based on first passage probabilities". FPPM is implemented in FPPM.py.

# Dependence
* python3
* networkx
* python-igraph
* numpy
* pandas
* scipy
* plotly
* [LFR program](https://sites.google.com/site/santofortunato/benchmark.tgz)

# Simulations
To repeat our numerical experiments, run as follows:
* Simulations on Planted L-Partition Benchmarks
  1. python generate_planted_lpartition.py
  2. python Simulation_on_Planted_LPartition.py
* Simulations on LFR Benchmarks
  1. python generate_lfr.py
  2. python Simulation_on_LFR.py
* Simulations on Real  Networks
  1. cd Real_Networks
  2. python preprocess.py
  3. cd ..
  4. python Simulation_on_Real_Networks.py
* Visualization
  1. python visualize.py

Due to randomness, the results maybe not be reproduced in the simulations on the synthetic benchmarks. But the results must be similar. Our computer configuration is Intel(R) Core(TM) i5-4200H CPU @ 2.80GHz with 8 GB RAM. Three simulations cost nearly 10 minutes, 5 hours and 25 minutes.