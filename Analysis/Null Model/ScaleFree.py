import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from SnapAnalysis import SnapAnalysis
import json
import snap

G = snap.GenRndPowerLaw(11528, 4.025269688407503)


#Degree distribution
degrees = [node.GetOutDeg() + node.GetInDeg() for node in G.Nodes()]
kmin = min(degrees)
kmax = max(degrees)


# Get 10 logarithmically spaced bins between kmin and kmax
bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=100)

# histogram the data into these bins
density, _ = np.histogram(degrees, bins=bin_edges, density=True)

ig = plt.figure(figsize=(10, 10))

# "x" should be midpoint (IN LOG SPACE) of each bin
log_be = np.log10(bin_edges)
x = 10**((log_be[1:] + log_be[:-1])/2)

plt.loglog(x, density, marker='o', linestyle='none')
plt.xlabel(r"degree $k$", fontsize=16)
plt.ylabel(r"$P(k)$", fontsize=16)

# remove right and top boundaries because they're ugly
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Show the plot
plt.show()

edges = []
for e in G.Edges():
    edges.append([e.GetSrcNId(), e.GetDstNId()])

nodes= []
for n in G.Nodes():
    nodes.append(n.GetId())

results = SnapAnalysis(nodes, edges)

with open('./DataStats/ScaleFree.json','w+') as f:
    json.dump(results,f)