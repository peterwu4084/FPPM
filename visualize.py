import os
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

if not os.path.exists('Visualization'):
    os.mkdir('Visualization')
    
names = ['Fastgreedy', 'Infomap', 'LPA', 'Louvein', 'Walktrap', 'FPPM']
symbols = ['circle', 'square', 'diamond', 'x', 'triangle-left', 'star']
colors = px.colors.qualitative.Set1

# Planted l-partition benchmarks
with open('Planted_LPartition_benchmarks/Fastgreedy_performance.pickle', 'rb') as f:
    Fastgreedy_performance = pickle.load(f)
    Fastgreedy_performance[0] = np.reshape(Fastgreedy_performance[0], (9, 10000)).mean(axis=1)
    Fastgreedy_performance[1] = np.reshape(Fastgreedy_performance[1], (12, 10000)).mean(axis=1)
with open('Planted_LPartition_benchmarks/Infomap_performance.pickle', 'rb') as f:
    Infomap_performance = pickle.load(f)
    Infomap_performance[0] = np.reshape(Infomap_performance[0], (9, 10000)).mean(axis=1)
    Infomap_performance[1] = np.reshape(Infomap_performance[1], (12, 10000)).mean(axis=1)
with open('Planted_LPartition_benchmarks/LPA_performance.pickle', 'rb') as f:
    LPA_performance = pickle.load(f)
    LPA_performance[0] = np.reshape(LPA_performance[0], (9, 10000)).mean(axis=1)
    LPA_performance[1] = np.reshape(LPA_performance[1], (12, 10000)).mean(axis=1)
with open('Planted_LPartition_benchmarks/Louvein_performance.pickle', 'rb') as f:
    Louvein_performance = pickle.load(f)
    Louvein_performance[0] = np.reshape(Louvein_performance[0], (9, 10000)).mean(axis=1)
    Louvein_performance[1] = np.reshape(Louvein_performance[1], (12, 10000)).mean(axis=1)
with open('Planted_LPartition_benchmarks/Walktrap_performance.pickle', 'rb') as f:
    Walktrap_performance = pickle.load(f)
    Walktrap_performance[0] = np.reshape(Walktrap_performance[0], (9, 10000)).mean(axis=1)
    Walktrap_performance[1] = np.reshape(Walktrap_performance[1], (12, 10000)).mean(axis=1)
with open('Planted_LPartition_benchmarks/FPPM_performance.pickle', 'rb') as f:
    FPPM_performance = pickle.load(f)
    FPPM_performance[0] = np.reshape(FPPM_performance[0], (9, 10000)).mean(axis=1)
    FPPM_performance[1] = np.reshape(FPPM_performance[1], (12, 10000)).mean(axis=1)

fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
traces = [Fastgreedy_performance, Infomap_performance, LPA_performance,
    Louvein_performance, Walktrap_performance, FPPM_performance]
for idx, trace in enumerate(traces):
    fig.add_trace(go.Scatter(
        x=list(range(9, 18)),
        y = trace[0],
        mode='markers+lines',
        marker_symbol=symbols[idx]+'-dot',
        marker_size=15,
        marker_opacity=0.8,
        marker_color=colors[idx],
        name=names[idx]
        ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(
        x=list(range(4, 16)),
        y=trace[1],
        mode='markers+lines',
        marker_symbol=symbols[idx]+'-dot',
        marker_size=15,
        marker_opacity=0.8,
        marker_color=colors[idx],
        name=names[idx],
        showlegend=False
        ),
        row=1,
        col=2)
fig.update_xaxes(title_text='$Internal Degree$', row=1, col=1)
fig.update_xaxes(title_text='$Internal Degree$', row=1, col=2)
fig.update_yaxes(title_text='Normalised Mutual Infomation', row=1, col=1)
fig.update_layout(title='Simulations on Planted L-partition Benchmarks',
    margin=dict(b=0, l=0, r=0, t=50, pad=0), height=400, width=1000)
fig.write_html('Visualization/Visual_Planted_LPartition.html')
fig.write_image('Visualization/Planted_LPartition_benchmarks.eps')
# LFR benchmarks
with open('LFR_benchmarks/Fastgreedy_performance.pickle', 'rb') as f:
    Fastgreedy_performance = pickle.load(f)
    for _ in range(3):
        Fastgreedy_performance[_] = np.reshape(Fastgreedy_performance[_], (9, 10000)).mean(axis=1)
with open('LFR_benchmarks/Infomap_performance.pickle', 'rb') as f:
    Infomap_performance = pickle.load(f)
    for _ in range(3):
        Infomap_performance[_] = np.reshape(Infomap_performance[_], (9, 10000)).mean(axis=1)
with open('LFR_benchmarks/LPA_performance.pickle', 'rb') as f:
    LPA_performance = pickle.load(f)
    for _ in range(3):
        LPA_performance[_] = np.reshape(LPA_performance[_], (9, 10000)).mean(axis=1)
with open('LFR_benchmarks/Louvein_performance.pickle', 'rb') as f:
    Louvein_performance = pickle.load(f)
    for _ in range(3):
        Louvein_performance[_] = np.reshape(Louvein_performance[_], (9, 10000)).mean(axis=1)
with open('LFR_benchmarks/Walktrap_performance.pickle', 'rb') as f:
    Walktrap_performance = pickle.load(f)
    for _ in range(3):
        Walktrap_performance[_] = np.reshape(Walktrap_performance[_], (9, 10000)).mean(axis=1)
with open('LFR_benchmarks/FPPM_performance.pickle', 'rb') as f:
    FPPM_performance = pickle.load(f)
    for _ in range(3):
        FPPM_performance[_] = np.reshape(FPPM_performance[_], (9, 10000)).mean(axis=1)

fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.01)
traces = [Fastgreedy_performance, Infomap_performance, LPA_performance,
    Louvein_performance, Walktrap_performance, FPPM_performance]
for idx, trace in enumerate(traces):
    fig.add_trace(go.Scatter(
        x=[_ / 10 for _ in range(1, 10)],
        y = trace[0],
        mode='markers+lines',
        marker_symbol=symbols[idx]+'-dot',
        marker_size=15,
        marker_opacity=0.8,
        marker_color=colors[idx],
        name=names[idx]
        ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(
        x=[_ / 10 for _ in range(1, 10)],
        y=trace[1],
        mode='markers+lines',
        marker_symbol=symbols[idx]+'-dot',
        marker_size=15,
        marker_opacity=0.8,
        marker_color=colors[idx],
        name=names[idx],
        showlegend=False
        ),
        row=1,
        col=2)
    fig.add_trace(go.Scatter(
        x=[_ / 10 for _ in range(1, 10)],
        y=trace[2],
        mode='markers+lines',
        marker_symbol=symbols[idx]+'-dot',
        marker_size=15,
        marker_opacity=0.8,
        marker_color=colors[idx],
        name=names[idx],
        showlegend=False
        ),
        row=1,
        col=3)
fig.update_xaxes(title_text='Mixing Parameter', row=1, col=1)
fig.update_xaxes(title_text='Mixing Parameter', row=1, col=2)
fig.update_xaxes(title_text='Mixing Parameter', row=1, col=3)
fig.update_yaxes(title_text='Normalised Mutual Infomation', row=1, col=1)
fig.update_layout(title='Simulations on LFR Benchmarks',
    margin=dict(b=0, l=0, r=0, t=50, pad=0), height=300, width=1000)
fig.write_html('Visualization/Visual_LFR.html')
fig.write_image('Visualization/LFR_benchmarks.eps')

# Real networks
with open('Real_Networks/Fastgreedy_performance.pickle', 'rb') as f:
    Fastgreedy_performance = np.mean(pickle.load(f), axis=1)
with open('Real_Networks/Infomap_performance.pickle', 'rb') as f:
    Infomap_performance = np.mean(pickle.load(f), axis=1)
with open('Real_Networks/LPA_performance.pickle', 'rb') as f:
    LPA_performance = np.mean(pickle.load(f), axis=1)
with open('Real_Networks/Louvein_performance.pickle', 'rb') as f:
    Louvein_performance = np.mean(pickle.load(f), axis=1)
with open('Real_Networks/Walktrap_performance.pickle', 'rb') as f:
    Walktrap_performance = np.mean(pickle.load(f), axis=1)
with open('Real_Networks/FPPM_performance.pickle', 'rb') as f:
    FPPM_performance = np.mean(pickle.load(f), axis=1)

d = {'Fastgreedy': Fastgreedy_performance,
    'Infomap': Infomap_performance,
    'LPA': LPA_performance,
    'Louvein': Louvein_performance,
    'Walktrap': Walktrap_performance,
    'FPPM': FPPM_performance
}
df = pd.DataFrame(d, index=['Polblogs', 'Polbooks', 'Cora', 'Citeseer'])
df.to_csv('Visualization/Visual_Real_Networks.csv')
