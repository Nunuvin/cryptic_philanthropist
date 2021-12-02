import pandas as pd
import networkx as nx

df_edge = pd.read_csv('../../Gephi/Gephi_Edge_List.csv', dtype=str)
df_node = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)


G = nx.from_pandas_edgelist(
    df_edge, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())

# attrs = {}
# # Set node attributes
# for index, row in df_node.iterrows():
#     ls = row.values.tolist()
#     attrs[row['Id']] = {'PostID': ls[1], 'Size': ls[3], 'ModClass': ls[4]}

# nx.set_node_attributes(G, attrs)

# Calculate basic stats
#original_avg_path = nx.average_shortest_path_length(G, weight='edge_attr')
#original_clustering = nx.average_clustering(G, weight='edge_attr')

# print(original_avg_path)
# print(original_clustering)

for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
    print(nx.average_shortest_path_length(C))
