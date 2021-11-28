import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.centrality.betweenness import betweenness_centrality
from networkx.algorithms.centrality.closeness import closeness_centrality
from networkx.algorithms.centrality.degree_alg import degree_centrality
from networkx.algorithms.centrality.eigenvector import eigenvector_centrality
from networkx.algorithms.link_prediction import common_neighbor_centrality
from networkx.generators import community
import numpy as np
import random
import pandas as pd
from collections import defaultdict

df_edge = pd.read_csv('../../Gephi/Gephi_Edge_List.csv')
df_node = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv')

#print(df_node)
#dfmod_class = df_node[df_node['modularity_class'] == 4]
#print(dfmod_class)

G = nx.Graph()

#add edges and edge attributes
for i, edge_row in df_edge.iterrows():
    G.add_edge(edge_row[0], edge_row[1], weight = edge_row[6])

#add node attributes
for i, node_row in df_node.iterrows():
    G.add_node(node_row[0], modularity = int(node_row[4]))
#print(G.nodes(data="modularity"))

degrees = degree_centrality(G)
#closeness = closeness_centrality(G)
#eigen = eigenvector_centrality(G)
#betweeness = betweenness_centrality(G)

#print(degrees)
#print(closeness)
#print(eigen)

community_degree ={}
community_closeness = {}
community_eigen = {}
community_betweeness ={}
node_degree = {}
node_closeness = {}
node_eigen = {}
node_betweeness ={}
mod_class = []

community = 0
for index, row in df_node.iterrows():
    #if row['modularity_class'] == 4:
        community = row['modularity_class']
        node_degree.update({row['Id']: degrees.get(row['Id'])})
        #node_closeness.update({row['Id']: closeness.get(row['Id'])})
        #node_eigen.update({row['Id']: eigen.get(row['Id'])})
        #node_betweeness.update({row['Id']: betweeness.get(row['Id'])})
community_degree[community] = node_degree
#community_closeness[community] = node_closeness
#community_eigen[community] = node_eigen
#community_betweeness[community] = node_betweeness

#for id in dfmod_class['Id']:
    #community_degree.update({id: degrees.get(id)})
print(community_degree)
#print(community_closeness)
#print(community_eigen)
#print(community_betweeness)

