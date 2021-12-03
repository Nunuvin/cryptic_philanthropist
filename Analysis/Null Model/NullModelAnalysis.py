
import networkx as nx
import time
from multiprocessing import Pool

path_total = 0
clustering_total = 0

EDGE_LIST = '../../Gephi/nx_edges_list.csv'

G = None

with open(EDGE_LIST, 'r') as fhEdge:
    G = nx.read_weighted_edgelist(fhEdge, delimiter=',')
# print(G)
# G = nx.from_pandas_edgelist(
#     df_edge, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())

G = [G.subgraph(c).copy()
     for c in nx.connected_components(G)][0]



def computeVariables(a):
    global path_total, clustering_total, G

    NUM_EDGES = 155416

    G1 = nx.Graph(G)
    start_time = time.time()
    nx.double_edge_swap(G1, nswap=NUM_EDGES, max_tries=NUM_EDGES*10)

    avg_path = nx.average_shortest_path_length(G1, weight='edge_attr')
    clustering = nx.average_clustering(G1, weight='edge_attr')

    
 #   path_total += avg_path
 #   clustering_total += clustering
    print("Process died: ", a)
    return (avg_path, clustering)
#    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    simCount = 100
    sol = [i for i in range(0, simCount)]
    arr = []
    with Pool(24) as p:
        arr = p.map(computeVariables, sol)

    path_total = sum(p[0] for p in arr) / simCount
    clustering_total = sum(p[1] for p in arr) / simCount
    print("path_total: ",  path_total)
    print("cluster_total: ", clustering_total)
