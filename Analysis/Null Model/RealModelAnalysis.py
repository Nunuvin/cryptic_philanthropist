import pandas as pd
import networkx as nx
from SnapAnalysis import SnapAnalysis
import json

df_edge = pd.read_csv('../../Gephi/Gephi_Edge_List.csv')
df_node = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv')

all_nodes = df_node['Id'].values.tolist()
all_edges = df_edge[['Source', 'Target', 'Weight']].values.tolist()

print(all_nodes)

results = SnapAnalysis(all_nodes, all_edges)

with open('./DataStats/Real_Model.json', 'w') as f:
    json.dump(results, f)