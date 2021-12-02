import networkx as nx
from networkx.generators import directed
import pandas as pd

df = pd.read_csv('../../Gephi/Authors/Gephi_Author_Edge_List.csv', dtype=str)
df_node = pd.read_csv(
    '../../Gephi/Authors/Gephi_Author_Nodes_List.csv', dtype=str)

G = nx.from_pandas_edgelist(
    df, source="Source", target="Target", edge_attr='Weight', create_using=nx.DiGraph())

in_deg = sorted(G.in_degree, key=lambda x: x[1], reverse=True)

out_deg = sorted(G.out_degree, key=lambda x: x[1], reverse=True)

print(' ------- MOST IN DEGREE -------')
for i in range(0, 10):
    val = in_deg[i][0]
    print((df_node.loc[df_node['Id'] == val]).iloc[0]
          ['Label'] + " --> " + str(in_deg[i][1]))

print(' ------- MOST OUT DEGREE -------')
for i in range(0, 10):
    val = out_deg[i][0]
    print((df_node.loc[df_node['Id'] == val]).iloc[0]
          ['Label'] + " --> " + str(out_deg[i][1]))
