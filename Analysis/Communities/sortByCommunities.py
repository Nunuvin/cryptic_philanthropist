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
    with open('./Community_Hashtags.json', 'w') as outfile:
        output = {}
        res = {}
        for Communities, hashtags in out.items():
            hashtagCount = {}
            highest = {}
            topTen ={}
            max = 0
            tag = " "
            #print(Communities)
            #if Communities == '1':
                #print(Community)
            for hashtag in hashtags:
                if hashtag in hashtagCount:
                    count = hashtagCount[hashtag] + 1
                    #if count > max:
                    #    max = count
                    #    tag = hashtag     
                    hashtagCount.update({hashtag: count})
                    #print(hashtagCount)
                else:
                    hashtagCount[hashtag] = 1
                    count = 1
                    #if count > max:
                    #    max = count
                    #    tag = hashtag
            topTen = dict(sorted(hashtagCount.items(), key=lambda x:x[1], reverse=True))
            for x in list(topTen)[0:10]:
                highest[x] = topTen[x]
            output[Communities] = topTen
            res[Communities] = highest
        json_object = json.dumps(output)
        outfile.write(json_object)
    print(res)

findCommonHashtags()
countHashtags()