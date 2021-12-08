import pandas as pd
import json
from dateutil import parser as dateParser

df_nodes = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)
df_edges= pd.read_csv('../../Gephi/Gephi_Edge_List.csv', dtype=str)

with open('../../Outputs/final_giveaways_dict.json','r') as f:
    posts_att = json.load(f)

mod_to_time = {}

for index, row in df_edges.iterrows():
    s_m = int(df_nodes.loc[df_nodes['Id'] == row['Source']].iloc[0]['modularity_class'])
    t_m = int(df_nodes.loc[df_nodes['Id'] == row['Target']].iloc[0]['modularity_class'])

    if s_m == t_m:
        #Calculate delta time
        s_label = df_nodes.loc[df_nodes['Id'] == row['Source']].iloc[0]['Label']
        t_label = df_nodes.loc[df_nodes['Id'] == row['Target']].iloc[0]['Label']
        
        try:
            result = abs((dateParser.isoparse(posts_att[s_label]['created_at'])) - (dateParser.isoparse(posts_att[t_label]['created_at'])))
            
            if s_m in mod_to_time:
                mod_to_time[s_m] = [mod_to_time[s_m][0] + result.total_seconds(), mod_to_time[s_m][1] + 1]
            else:
                mod_to_time[s_m] = [result.total_seconds(),1]

            #print('calculation done')

        except Exception as e:
            #print(e)
            pass


with open('./Community_to_delta_time.json','w+') as f:
    json.dump(mod_to_time, f)