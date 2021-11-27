import pandas as pd
import json
import re

NODE_LIST_FILE = "./Gephi/Gephi_Nodes_List.csv"
IN_FILE_NAME = "./Outputs/Giveaway_tweets_info.json"

df = pd.read_csv(NODE_LIST_FILE, dtype=str)

f = open(IN_FILE_NAME,)
out = {}

giveaways = json.load(f)

def findCommonHashtags():
    for index, row in df.iterrows():
        #print(row)
        try:
            text = giveaways[row['Label']]['text']
            hashtag_list = re.findall("#[A-z0-9]+", text)
            #print(hashtag_list)
            
            
            if row['modularity_class'] in out:
                out[row['modularity_class']] = out[row['modularity_class']] + hashtag_list
            else:
                out[row['modularity_class']] = hashtag_list
            #print(out)
        except KeyError:
            pass
       
        

def countHashtags():
    with open('./Outputs/Community_Hashtags.json', 'w') as outfile:
        output = {}
        for Communities, hashtags in out.items():
            hashtagCount = {}
            #print(Communities)
            #if Communities == '1':
                #print(Community)
            for hashtag in hashtags:
                if hashtag in hashtagCount:
                    count = hashtagCount[hashtag] + 1
                    #print(count)
                    hashtagCount.update({hashtag: count})
                    #print(hashtagCount)
                else:
                    hashtagCount[hashtag] = 1
            output[Communities] = hashtagCount
        json_object = json.dumps(output)
        outfile.write(json_object)
    #print(hashtagCount)
    
findCommonHashtags()
countHashtags()