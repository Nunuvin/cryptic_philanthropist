
import json
from multiprocessing import Pool
from SnapAnalysis import SnapAnalysis
from EdgeSwap import EdgeSwap

def computeVariables(a):

    all_edges = EdgeSwap()

    all_nodes = list(range(0, 11529))

    results = SnapAnalysis(all_nodes, all_edges)

    with open('./DataStats/Null_Model_' + str(a) + ".json", 'w') as f:
        json.dump(results, f)

    #print("# ",a," is complete")
    

    path_total = sum(p[0] for p in arr) / simCount
    clustering_total = sum(p[1] for p in arr) / simCount
    print("path_total: ",  path_total)
    print("cluster_total: ", clustering_total)
    end = datetime.now()
    print("Program ended: ", end)
    print("Delta run time: ", end - start)
