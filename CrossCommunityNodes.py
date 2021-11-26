import pandas as pd
import json

NODE_LIST_FILE = "./Gephi/Gephi_Nodes_List.csv"
EDGE_LIST_FILE = "./Gephi/Gephi_Edge_List.csv"

df = pd.read_csv(NODE_LIST_FILE)
df_edge = pd.read_csv(EDGE_LIST_FILE)

cross_community_list = {}

for index, row in df_edge.iterrows():
    if df['modularity_class'][row['Source']] != df['modularity_class'][row['Target']]:
        label = str(df['Label'][row['Source']])

        if label in cross_community_list:
            ls = cross_community_list[label]['Target modularity']
            target = str(df['modularity_class'][row['Target']])

            if target not in ls:
                ls.append(target)

                cross_community_list[label] = {
                    'Original': str(cross_community_list[label]['Original']), 'Target modularity': ls}

        else:
            cross_community_list[label] = {'Original': str(df['modularity_class'][row['Source']]), 'Target modularity': [
                str(df['modularity_class'][row['Target']])]}


with open('./Gephi/Node_to_community.json', 'w') as fp:
    json.dump(cross_community_list, fp)
