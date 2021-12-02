import pandas as pd
import networkx as nx
import time
import threading

path_total = 0
clustering_total = 0

df_edge = pd.read_csv('../../Gephi/Gephi_Edge_List_FILTERED.csv', dtype=str)
#df_node = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)


G = nx.from_pandas_edgelist(
    df_edge, source="Source", target="Target", edge_attr='Weight', create_using=nx.Graph())

G = [G.subgraph(c).copy()
     for c in nx.connected_components(G)][0]

mutex = threading.Lock()


def computeVariables():
    global path_total, clustering_total, G, mutex

    NUM_EDGES = 15

    G1 = nx.Graph(G)

    start_time = time.time()
    nx.double_edge_swap(G1, nswap=NUM_EDGES, max_tries=NUM_EDGES*10)

    avg_path = nx.average_shortest_path_length(G1)
    clustering = nx.average_clustering(G1, weight='edge_attr')

    mutex.acquire()
    path_total += avg_path
    clustering_total += clustering
    mutex.release()

    print("--- %s seconds ---" % (time.time() - start_time))


threads = []
# Do 1000 times
for i in range(0, 1):
    x = threading.Thread(target=computeVariables, args=())
    x.start()
    threads.append(x)

for thread in threads:
    thread.join()


print(path_total/100)
print(clustering_total/100)
