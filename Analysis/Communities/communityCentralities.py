import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool
from networkx.algorithms.centrality.betweenness import betweenness_centrality
from networkx.algorithms.centrality.closeness import closeness_centrality
from networkx.algorithms.centrality.degree_alg import degree_centrality
from networkx.algorithms.centrality.eigenvector import eigenvector_centrality
from networkx.algorithms.link_prediction import common_neighbor_centrality
from networkx.generators import community
import numpy as np
import random
import pandas as pd
import json
import itertools
from collections import defaultdict

df_edge = pd.read_csv('../../Gephi/Gephi_Edge_List.csv', dtype=str)
df_node = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)

#print(df_node)
#dfmod_class = df_node[df_node['modularity_class'] == 4]
#print(dfmod_class)

#G = nx.Graph()

#add edges and edge attributes
#for i, edge_row in df_edge.iterrows():
   # G.add_edge(edge_row[0], edge_row[1], weight = edge_row[6])
G = nx.from_pandas_edgelist(
    df_edge, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())
data = df_node.set_index('Label').to_dict('index').items()
G.add_nodes_from(data)
#add node attributes
#for i, node_row in df_node.iterrows():
    #G.add_node(node_row[0], modularity = str(node_row[4]))
#print(G.nodes(data="modularity"))

#degrees = degree_centrality(G)
#closeness = closeness_centrality(G)
#eigen = eigenvector_centrality(G)
#betweeness = betweenness_centrality(G, k=1000)

community_degree ={}
community_closeness = {}
community_eigen = {}
community_betweeness ={}


community = 0

def degree_centrality():
    for index, row in df_node.iterrows():
        postID = str(row['Label'])
        community = row['modularity_class']
        if community not in community_degree:
            community_degree[community] = {postID: degrees.get(row['Id'])}
        else:
            degs = community_degree[community]
            degs.update({postID: degrees.get(row['Id'])})
            community_degree.update({community: degs})
    with open('./degrees.json', 'w+') as d:
        json.dump(community_degree, d)


def closen_centrality():
    for index, row in df_node.iterrows():
        postID = str(row['Label'])
        community = row['modularity_class']
        if community not in community_closeness:
            community_closeness[community] = {postID: closeness.get(row['Id'])}
        else:
            closes = community_closeness[community]
            closes.update({postID: closeness.get(row['Id'])})
            community_closeness.update({community: closes})
    with open('./closeness.json', 'w+') as c:
        json.dump(community_closeness, c)

def eigen_centrality():
    for index, row in df_node.iterrows():
        postID = str(row['Label'])
        community = row['modularity_class']
        if community not in community_eigen:
            community_eigen[community] = {postID: eigen.get(row['Id'])}
        else:
            eigens = community_eigen[community]
            eigens.update({postID: eigen.get(row['Id'])})
            community_eigen.update({community: eigens})
    with open('./eigen.json', 'w+') as e:
        json.dump(community_eigen, e)

def betweeness_centrality():
    for index, row in df_node.iterrows():
        postID = str(row['Label'])
        community = row['modularity_class']
        if community not in community_betweeness:
            community_betweeness[community] = {postID: betweeness.get(row['Id'])}
        else:
            betweens = community_betweeness[community]
            betweens.update({postID: betweeness.get(row['Id'])})
            community_betweeness.update({community: betweens})
    with open('./betweeness_unweighted.json', 'w+') as b:
        json.dump(community_betweeness, b)

#does not work
def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x

#does not work :(
def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.starmap(
        nx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks,
        ),
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

#degree_centrality()
#closen_centrality()
#eigen_centrality()
#betweeness_centrality()
#betweenness_centrality_parallel(G)
