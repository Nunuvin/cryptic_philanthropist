import json
from dotenv import load_dotenv
import os
import time
import requests

#GLOBALS
load_dotenv()
envBear = {}
envBear['BEARER_TOKEN'] = os.getenv('BEARER_TOKEN')

GIVEAWAY_FILE_IN = './Outputs/final_giveaways.json'
DELETED_TWEETS = "./Outputs/deleted_tweets.log"
PARENT_TWEET_AUTHORS = "./Outputs/authors.json"


refs = []
included = []
#END OF GLOBALS

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

def get_tweet_info(id):
    url = "https://api.twitter.com/2/tweets?ids=" + id + \
    "&tweet.fields=conversation_id,in_reply_to_user_id,author_id,source,text,id,public_metrics,created_at,geo,referenced_tweets,withheld"
    return requests.get(url, auth=bearer_oauth)

def get_missing_tweets():
    global GIVEAWAY_FILE_IN, refs, included
    with open(GIVEAWAY_FILE_IN, 'r') as infile:
        giveaway_dict = json.load(infile)

    for obj in giveaway_dict:
        try:
            refs.append(obj['referenced_tweets'][0]['id'])
        except KeyError:
            included.append(obj['id'])

    refs = dict.fromkeys(refs)
    included = dict.fromkeys(included)

    return list(set(refs) - set(included))

def main():
    

    missing = get_missing_tweets()

    print(len(missing))
    with open(DELETED_TWEETS,"w+") as dellog:
        with open(PARENT_TWEET_AUTHORS,"w+") as data:
            data.writelines("[")
            for i,val in enumerate(missing):
                r = get_tweet_info(val)
                if "errors" in r.json().keys():
                    dellog.write(val)
                    dellog.write('\n')
                else:
                    #print(r.json())
                    data.write(json.dumps(r.json()))
                    print(i/len(missing)*100)
                    data.write(",")
                time.sleep(1)
                
            data.writelines("]")

if __name__=="__main__":
    main()