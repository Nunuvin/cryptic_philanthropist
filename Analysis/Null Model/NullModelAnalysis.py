
import json
from multiprocessing import Pool

import numpy as np
from SnapAnalysis import SnapAnalysis
from EdgeSwap import EdgeSwap
import pandas as pd
from dateutil import parser as dateParser
from datetime import timedelta

def computeVariables(a):

    df_nodes = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)

    with open ('../../Outputs/Giveaway_tweets_info.json', 'r') as f:
        tweets=json.load(f)

    all_edges = EdgeSwap()

    all_nodes = list(range(0, 11529))

    #Sort by weight
    all_edges_sorted = sorted(all_edges, key=lambda x: x[2], reverse=True)
    #Get average for top 100
    delta_total = timedelta()
    valid_pairs = 0
    for i in range(0,100):
        try:
            node_one = df_nodes.loc[df_nodes['Id'] == str(all_edges_sorted[i][0])].iloc[0]['Label']
            node_two = df_nodes.loc[df_nodes['Id'] == str(all_edges_sorted[i][1])].iloc[0]['Label']

            delta_total += dateParser.isoparse(tweets[node_one]['created_at']) - dateParser.isoparse(tweets[node_two]['created_at'])
            valid_pairs += 1

        except Exception as e:
            print("Key not found!")

    delta_avg = None
    if valid_pairs > 0:
        delta_avg = delta_total.total_seconds()/valid_pairs


    results = SnapAnalysis(all_nodes, all_edges)
    results['Delta_time'] = delta_avg

    with open('./DataStats/Null_Model_' + str(a) + ".json", 'w+') as f:
        json.dump(results, f)

    print(" -----  Null Model #" + str(a) + " has finished ----- ")
    

if __name__ == '__main__':
    simCount = 1
    sol = [1 for i in range(0, simCount)]
    arr = []
    with Pool(32) as p:
        arr = p.map(computeVariables, sol)
