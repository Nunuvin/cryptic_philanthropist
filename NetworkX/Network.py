import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from collections import defaultdict
import powerlaw

df = pd.read_csv('../Outputs/EdgeList.csv')

# read in an edge list from the file 'test.txt'
G = nx.from_pandas_edgelist(
    df, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())

# nodes = pd.read_csv('../Outputs/NodeList.csv', sep=',')
# data = nodes.set_index('ID').to_dict('index').items()
# G.add_nodes_from(data)


degrees = [G.degree(node) for node in G]
kmin = min(degrees)
kmax = max(degrees)


fit = powerlaw.Fit(degrees) 

print("Estimated power law exponent = " + fit.power_law.alpha)

fig2 = fit.plot_pdf(color='b', linewidth=2)
fit.power_law.plot_pdf(color='g', linestyle='--', ax=fig2)

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
