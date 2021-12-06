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
        avg_clustering = 0
        avg_closeness = 0
        avg_eigen = 0
        avg_shortest_path = 0

        Nodes, Edges = G.GetBetweennessCentr(1.0)
        for node in Nodes:
            avg_betweeness += Nodes[node]

        avg_betweeness /= G.GetNodes()

        avg_clustering = G.GetClustCf()

        #Closeness centrality
        for NI in G.Nodes():
            avg_closeness += G.GetClosenessCentr(NI.GetId())
        
        avg_closeness /= G.GetNodes()


        NIdEigenH = G.GetEigenVectorCentr()
        for item in NIdEigenH:
            avg_eigen += NIdEigenH[item]
        
        avg_eigen /= G.GetNodes()


        avg_shortest_path = G.GetBfsEffDiam(G.GetNodes(), all_nodes, False)

        print("--- %s seconds ---" % (time.time() - start_time))

        return {"betweenss" : avg_betweeness, "clustering" : avg_clustering, "closeness": avg_closeness, "eigen" : avg_eigen, "path" : avg_shortest_path}
    except Exception as e:
        print(e)
        print("--- %s seconds ---" % (time.time() - start_time))