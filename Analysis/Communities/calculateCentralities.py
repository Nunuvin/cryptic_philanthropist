import pandas as pd
import json

NODE_LIST_FILE = "../../Gephi/Gephi_Nodes_List.csv"
CALC_FILE = "../Null Model/DataStats/Real_model.json"

df = pd.read_csv(NODE_LIST_FILE, dtype=str)

f = open(CALC_FILE,)
out = {}

centralities = json.load(f)

def getValues():
    
    for index, row in df.iterrows():
        betweenness = centralities['node_to_betweeness'][row['Id']]
        closeness = centralities['node_to_closeness'][row['Id']]
        eigen = centralities['node_to_eigen'][row['Id']]
        mod = row['modularity_class']
        #print("at if")
        if mod in out:
            out[mod]["betweeness"][row["Label"]] = betweenness 
            out[mod]["closeness"][row["Label"]] = closeness 
            out[mod]["eigen"][row["Label"]] = eigen
            
        else:
            out[mod] = {}
            out[mod]["betweeness"] = {row["Label"]:betweenness} 
            out[mod]["closeness"] = {row["Label"]:closeness} 
            out[mod]["eigen"] = {row["Label"]:eigen}
    #print(out[mod])
    #centralitySort = dict(sorted(out[mod].items(), key=lambda x:x[1], reverse=True))
    for com in out:
        for bet in com:
            bets = out[bet]['betweeness']
            sortBets = dict(sorted(bets.items(), key=lambda x:x[1], reverse=True))
            out[bet]['betweeness'] = sortBets
        for closs in com:
            closses = out[closs]['closeness']
            sortCloss = dict(sorted(closses.items(), key=lambda x:x[1], reverse=True))
            out[closs]['closeness'] = sortCloss
        for eigen in com:
            eigens = out[eigen]['eigen']
            sortEigens = dict(sorted(eigens.items(), key=lambda x:x[1], reverse=True))
            out[eigen]['eigen'] = sortEigens
    
    #print(sortedBetsDict)
    with open('./communities_centralities.json', 'w+') as outfile:
        json.dump(out, outfile)
    #print(out)
getValues()