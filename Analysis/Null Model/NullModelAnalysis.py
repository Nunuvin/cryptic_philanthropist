
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

    print("# ",a," is complete")
    

if __name__ == '__main__':
    simCount = 100
    sol = [1 for i in range(0, simCount)]
    arr = []
    with Pool(32) as p:
        arr = p.map(computeVariables, sol)
