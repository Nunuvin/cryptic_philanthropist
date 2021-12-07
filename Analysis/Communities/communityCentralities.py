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

G = nx.from_pandas_edgelist(
    df_edge, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())
data = df_node.set_index('Label').to_dict('index').items()
G.add_nodes_from(data)
#add node attributes
#for i, node_row in df_node.iterrows():
    #G.add_node(node_row[0], modularity = str(node_row[4]))
#print(G.nodes(data="modularity"))

#-------------Note to make the calculation Faster, I only run one at a time!!!!!---------------
#degrees = degree_centrality(G)
#closeness = closeness_centrality(G)
#eigen = eigenvector_centrality(G)
betweeness = betweenness_centrality(G, k=1000)

community_degree ={}
community_closeness = {}
community_eigen = {}
community_betweeness ={}


avg_degree = 0;
avg_close = 0;
avg_eigen = 0;
avg_bet = 0;


community = 0

def degreeCentrality():
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


def closenessCentrality():
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

def eigenCentrality():
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

def betweennessCentrality():
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

def avgDegree():
    avgDeg_dict = {}
    for com, node in community_degree.items():
        avg_degree = 0
        for val in node.values():
            #print(val)
            try:
                avg_degree += val
            except TypeError:
                pass
        avg_degree = avg_degree/len(com)
        avgDeg_dict.update({com: avg_degree}) 
    print(avgDeg_dict)

def avgCloseness():
    avgClo_dict = {}
    for com, node in community_closeness.items():
        avg_close = 0
        for val in node.values():
            #print(val)
            try:
                avg_close += val
            except TypeError:
                pass
        avg_close = avg_close/len(com)
        avgClo_dict.update({com: avg_close}) 
    print(avgClo_dict)

def avgEigen():
    avgEig_dict = {}
    for com, node in community_eigen.items():
        avg_eigen = 0
        for val in node.values():
            #print(val)
            try:
                avg_eigen += val
            except TypeError:
                pass
        avg_eigen = avg_eigen/len(com)
        avgEig_dict.update({com: avg_eigen}) 
    print(avgEig_dict)

def avgBetween():
    avgBet_dict = {}
    for com, node in community_betweeness.items():
        avg_bet = 0
        for val in node.values():
            #print(val)
            try:
                avg_bet += val
            except TypeError:
                pass
        avg_bet = avg_bet/len(com)
        avgBet_dict.update({com: avg_bet}) 
    print(avgBet_dict)

#degreeCentrality()
#closenessCentrality()
#eigenCentrality()

#Warning, Betweenness takes forever to run (over 4 hours and it still was not complete)
betweennessCentrality()
#print("----------------------Average Degree for each community----------------------")
#avgDegree()
#print("----------------------Average Closeness for each community----------------------")
#avgCloseness()
#print("----------------------Average Eigen for each community----------------------")
#avgEigen()
print("----------------------Average betweenness for each community----------------------")
avgBetween()
