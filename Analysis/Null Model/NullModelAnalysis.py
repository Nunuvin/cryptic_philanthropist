
import json
from multiprocessing import Pool
from networkx.algorithms.traversal.depth_first_search import dfs_tree

import numpy as np
from SnapAnalysis import SnapAnalysis
from EdgeSwap import EdgeSwap
import pandas as pd
from dateutil import parser as dateParser
from datetime import timedelta

import networkx as nx

def computeVariables(a):

    df_nodes = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)
    df_edges = pd.read_csv("../../Gephi/Gephi_Edge_List.csv")
    #df_edges = pd.read_csv("./test_data.csv")

    G = nx.from_pandas_edgelist(df_edges, source="Source", target="Target", edge_attr="Weight", create_using=nx.Graph())
    all_edges = list(G.edges(data=True))
    

    print('----' + str(a) + ' has started')

    with open ('../../Outputs/Giveaway_tweets_info.json', 'r') as f:
        tweets=json.load(f)


    print('----' + str(a) + ' ---- Edge swap Started!')
    #all_edges = EdgeSwap()
    #nx.double_edge_swap(G, len(all_edges), len(all_edges)*5)

    df_edges['Target'] = np.random.permutation(df_edges['Target'].values)

    #Get all edges that have a self loop
    self_loops = df_edges.loc[df_edges['Source'] == df_edges['Target']]
    print(self_loops)
    if len(self_loops) > 0:
        for index, row in self_loops.iterrows():
            #Find an entry that does not have self loop with the source
            entries = df_edges.loc[(df_edges['Target'] != row['Source']) & (df_edges['Source'] != row['Source'])]
            selected_entry = entries.sample()
            replace_id = selected_entry.iloc[0]['Id']
            replace_value = selected_entry.iloc[0]['Target']
            original_value = row['Target']

            df_edges.at[row['Id'], 'Target'] = replace_value
            df_edges.at[replace_id, 'Target'] = original_value

    #Sort by the weight
    df_edges = df_edges.sort_values(by='Weight', ascending=False)

    #Convert to numpy array
    all_edges = df_edges[['Source', 'Target', 'Weight']].to_numpy(dtype=np.int64)
    
    
    #Assign weights based on the source, comparing it to the original
    # for e in G.edges(data=True):
    #     try:
    #         att = {'Weight' : df_edges.loc[df_edges['Source'] == e[0]].iloc[0]['Weight']}
    #         nx.set_edge_attributes(G, {(e[0],e[1]): att})
    #     except IndexError:
    #         att = {'Weight' : 0}
    #         nx.set_edge_attributes(G, {(e[0],e[1]): att})
    # print('----' + str(a) + ' ---- Edge swap complete!')

    all_nodes = list(range(0, len(df_nodes)))
    #all_nodes = list(range(0, 5))

    #Sort by weight
    #all_edges_sorted = sorted(all_edges, key=lambda x: x[2]['Weight'], reverse=True)
    #Get average for top 100
    delta_total = timedelta()
    valid_pairs = 0
    for i in range(0,100):
        try:
            node_one = df_nodes.loc[df_nodes['Id'] == str(all_edges[i][0])].iloc[0]['Label']
            node_two = df_nodes.loc[df_nodes['Id'] == str(all_edges[i][1])].iloc[0]['Label']
            
            delta_total += abs((dateParser.isoparse(tweets[node_one]['created_at'])) - (dateParser.isoparse(tweets[node_two]['created_at'])))
            valid_pairs += 1
        except IndexError:
            pass
        except Exception as e:
            print(e)
            print("Key not found for id1 = " + str(all_edges[i][0]) + " id2 = " + str(all_edges[i][1]))

    delta_avg = -1
    if valid_pairs > 0:
        delta_avg = abs(delta_total.total_seconds())/valid_pairs

    print('----' + str(a) + ' ---- Delta time calculation complete!')
    print('----' + str(a) + ' ---- Total avg = ' + str(delta_avg))
    results = {}
    results = SnapAnalysis(all_nodes, all_edges)
    results['Delta_time'] = delta_avg

    with open('./DataStats/Null_Model_' + str(a) + ".json", 'w+') as f:
        json.dump(results, f)


    print(" -----  Null Model #" + str(a) + " has finished ----- ")

    

if __name__ == '__main__':
    simCount = 100
    sol = list(range(0, simCount))

    # with Pool(10) as p:
    #     arr = p.map(computeVariables, sol)
    for i in range(0,simCount):
        computeVariables(i)
