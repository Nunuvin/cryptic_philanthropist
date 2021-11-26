import pandas as pd
import json
import re

NODE_LIST_FILE = "./Gephi/Gephi_Nodes_List.csv"
IN_FILE_NAME = "./Outputs/final_giveaways_dict.json"

df = pd.read_csv(NODE_LIST_FILE, dtype=str)

f = open(IN_FILE_NAME,)
out = {}

giveaways = json.load(f)

def findCommonHashtags():
    with open('./Outputs/Community_Hashtags.json', 'w') as outfile:
        for index, row in df.iterrows():
            #print(row)
            text = giveaways[row['Label']]['text']
            hashtag_list = re.findall("#[A-z0-9]+", text)
            #print(hashtag_list)
            
            if row['modularity_class'] in out:
                out[row['modularity_class']] = out[row['modularity_class']] + hashtag_list
            else:
                out[row['modularity_class']] = hashtag_list
            #print(out)

        json_object = json.dumps(out)
        outfile.write(json_object)
    
findCommonHashtags()