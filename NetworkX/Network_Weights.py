import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from collections import defaultdict

df = pd.read_csv('../Gephi/Gephi_Edge_List.csv')


weights = df['Weight'].values.tolist()
wmin = min(weights)
wmax = max(weights)


# Get 10 logarithmically spaced bins between kmin and kmax
bin_edges = np.logspace(np.log10(wmin), np.log10(wmax), num=100)

# histogram the data into these bins
density, _ = np.histogram(weights, bins=bin_edges, density=True)

ig = plt.figure(figsize=(10, 10))

# "x" should be midpoint (IN LOG SPACE) of each bin
log_be = np.log10(bin_edges)
x = 10**((log_be[1:] + log_be[:-1])/2)

plt.loglog(x, density, marker='o', linestyle='none')
plt.xlabel(r"Weight $w$", fontsize=16)
plt.ylabel(r"$P(w)$", fontsize=16)

# remove right and top boundaries because they're ugly
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Show the plot
plt.show()
