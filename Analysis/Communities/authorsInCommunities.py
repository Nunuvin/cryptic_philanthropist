import pandas as pd
import json
import re

NODE_LIST_FILE = "../../Gephi/Gephi_Nodes_List.csv"
IN_FILE_NAME = "../../Outputs/Giveaway_tweets_info.json"

df = pd.read_csv(NODE_LIST_FILE, dtype=str)

f = open(IN_FILE_NAME,)
out = {}

giveaways = json.load(f)

def findCommonHashtags():
    for index, row in df.iterrows():
        #print(row)
        try:
            author_list = giveaways[row['Label']]['author_id']
            #author_list = re.findall("#[A-z0-9]+", text)
            #print(author_list)
            
            
            if row['modularity_class'] in out:
                out[row['modularity_class']].append(author_list)
            else:
                out[row['modularity_class']] = [author_list]
            #print(out)
        except KeyError:
            pass
       
        

def countHashtags():
    with open('./Community_authors.json', 'w') as outfile:
        output = {}
        res = {}
        for Communities, authors in out.items():
            authorsCount = {}
            highest = {}
            max = 0
            tag = " "
            #print(Communities)
            #if Communities == '1':
                #print(Community)
            for author in authors:
                if author in authorsCount:
                    count = authorsCount[author] + 1
                    if count > max:
                        max = count
                        tag = author
                    #print(count)
                    authorsCount.update({author: count})
                else:
                    authorsCount[author] = 1
                    count = 1
                    if count > max:
                        max = count
                        tag = author
            highest[tag] = max
            output[Communities] = authorsCount
            res[Communities] = highest
        json_object = json.dumps(output)
        outfile.write(json_object)
    print(res)
    
findCommonHashtags()
countHashtags()