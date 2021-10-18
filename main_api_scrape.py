import requests
import json
from dotenv import load_dotenv
import os
import time
import datetime
import urllib

load_dotenv()
envBear = {}
envBear['BEARER_TOKEN'] = os.getenv('BEARER_TOKEN')

saveFiles = {
    "giveawayTweets" : "Outputs/giveaway.json"
}

# searchFollowupUrl = " https://api.twitter.com/2/tweets/search/recent?query=conversation_id:1445052091051876352&tweet.fields=in_reply_to_user_id,author_id,created_at,conversation_id&max_results=100&next_token=b26v89c19zqg8o3fpds84kv5lha4omoyjy3qvfhohy64d"




# def load_bearer_token():
#     '''
#     Reads .bear file and writes data into env dictionary
#     .bear Format:
#     bearer_token = TOKENVALUE
#     '''
#     global envBear
#     with open(".bear","r") as f:
#         lines = f.readlines()
#         for l in lines[1:]:
#             l = l.split(" ")
#             envBear[l[0]] = l[2]
#         #print(envBear)

def save_json_to_file(reqData):
    with open(saveFiles["giveawayTweets"], 'w+') as f:
                json.dump(reqData, f)

    # with open("Outputs/raw_data.csv","w+") as f:
    #     for entry in reqData:
    #         f.write(str(entry["id"]) + ', ' + str(entry["created_at"]) + ', ' + str(entry["public_metrics"]["reply_count"])+'\n')
    
    # exit()

def scrape_giveaways():
    '''
    Get those sweet giveaways
    '''
    global saveFiles

    tweetsByHashtag = "https://api.twitter.com/2/tweets/search/recent?query="+urllib.parse.quote_plus("((#crypto OR #cryptocurrency OR #nft) (#giveaway OR #giveaways)) OR (#cryptogiveaway OR #cryptogiveaways OR #nftgiveaway OR #nftgiveaways) OR ((crypto OR cryptocurrency OR nft) (giveaway OR giveaways))")+"&tweet.fields=conversation_id,in_reply_to_user_id,author_id,source,text,id,public_metrics,created_at,geo,referenced_tweets&max_results=100"

    # nasa_tweets = 'https://api.twitter.com/1.1/search/tweets.json?q=crypto%20giveaway&result_type=popular&since_id=1417454251299819520&count=15'
    # nasa_tweets2 = "https://api.twitter.com/1.1/search/tweets.json?max_id=1446475489359585283&q=nasa&include_entities=1&result_type=popular"

    #get first json
    
    # CHANGE LINE BELOW MBE
    th = tweetsByHashtag + '&next_token=' + "b26v89c19zqg8o3fpds9dvbpei8vgfonrifhb1lx0yet9"
    
    reqJson = get_req(saveFiles["giveawayTweets"], th, debug=False).json()
    #print(reqJson)
    
    reqData = reqJson["data"]
    #loop to get the rest
    apiLimit = 100
    MaxCnt = 3600
    i = 112
    nxt = False
    while i < MaxCnt:
        while (i % apiLimit != 0 and i < MaxCnt) or (nxt == True):
            nxt = False
            i += 1  
            
            try:
                nxtToken = reqJson["meta"]["next_token"]
            
            except Exception as e:
                print (nxtToken)
                print("issue at: ",i,"Error:\n")
                print(e)
                save_json_to_file(reqData)
                exit()

            print ("token: ", nxtToken, " i : ", i, " \% done: ", i/MaxCnt, " Time: ", datetime.datetime.fromtimestamp(time.time()))

            roundUrl = tweetsByHashtag + '&next_token=' + str(nxtToken)
            reqJson=get_req(saveFiles["giveawayTweets"], roundUrl, debug=False).json()
            reqData=reqJson["data"]

            # with open("Outputs/interm_"+str(i)+".json", 'w+') as f:
            #     json.dump(reqJson, f)
            

        # write to file
        #save_json_to_file(reqData)

            with open("Outputs/interm_%04d"%(i)+".json", 'w+') as f:
                json.dump(reqData, f)
            reqData = None

            time.sleep(7)
        

        if(i+1 >= MaxCnt):
            exit()
        nxt = True
        

    exit()
   

def main():
    #load_bearer_token() #load env vals
    scrape_giveaways()




def get_req(outputFilename, reqUrl, debug=False):
    r = requests.get(reqUrl, auth=bearer_oauth)
    if debug == False:
        return r
    else:
        print(r.json())



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {envBear['BEARER_TOKEN']}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

if __name__ == "__main__":
    main()