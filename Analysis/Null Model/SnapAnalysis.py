import snap
import time

def SnapAnalysis(all_nodes, all_edges):
    start_time = time.time()
    try:

        G = snap.TUNGraph.New()

        for n in all_nodes:
            G.AddNode(n)

        for e in all_edges:
            G.AddEdge(int(e[0]),int(e[1]))

        avg_betweeness = 0
        avg_betweeness_norm = 0
        avg_clustering = 0
        avg_closeness = 0
        avg_closeness_norm = 0
        avg_eigen = 0
        avg_shortest_path = 0

        Nodes, Edges = G.GetBetweennessCentr(1, False)
        for node in Nodes:
            #Normalize the betweeness centrality for each node
            #print(Nodes[node])
            avg_betweeness += Nodes[node]
            avg_betweeness_norm += (Nodes[node]/((G.GetNodes()-1)*(G.GetNodes()-2)/2))
            
        print('Computing betweeness...')
        avg_betweeness /= G.GetNodes()
        avg_betweeness_norm / G.GetNodes()
        print('Betweeness done')

        print('Computing clustering...')
        avg_clustering = G.GetClustCf()
        print('Clustering done')

        print('Computing closeness...')
        #Closeness centrality
        for NI in G.Nodes():
            avg_closeness += G.GetClosenessCentr(NI.GetId())
            avg_closeness_norm += G.GetClosenessCentr(NI.GetId())/(G.GetNodes() - 1)
        
        avg_closeness /= G.GetNodes()
        avg_closeness_norm /= G.GetNodes()

        print('Closeness done')

        # NIdEigenH = G.GetEigenVectorCentr()
        # for item in NIdEigenH:
        #     avg_eigen += NIdEigenH[item]
        
        # avg_eigen /= G.GetNodes()

        # print('Eigen done')

        print('Computing shortest path...')
        avg_shortest_path = G.GetBfsEffDiam(G.GetNodes(), all_nodes, False)

        print('Shortest path done')

        print("--- %s seconds ---" % (time.time() - start_time))

        return {"betweenss" : avg_betweeness, "betweeness_norm" : avg_betweeness_norm, "clustering" : avg_clustering, "closeness": avg_closeness, "closeness_norm": avg_closeness_norm, "eigen" : avg_eigen, "path" : avg_shortest_path}
    except Exception as e:
        print(e)
        print("--- %s seconds ---" % (time.time() - start_time))