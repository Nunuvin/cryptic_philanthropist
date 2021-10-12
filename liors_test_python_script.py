import requests
import json
from dotenv import load_dotenv
import os
import time
import urllib

load_dotenv()
envBear = {}
envBear['BEARER_TOKEN'] = os.getenv('BEARER_TOKEN')
fname = "Outputs/Liors_data_dump.json"

def get_req(outputFilename, reqUrl, debug=False):
    r = requests.get(reqUrl, auth=bearer_oauth)
    print(r.json())
    if debug == False:
        return r
    else:
        print(r.json())

def save_json_to_file(reqData):
    with open(fname, 'w+') as f:
                json.dump(reqData, f)

    # with open("Outputs/test_raw_data.csv","w+") as f:
    #     for entry in reqData:
    #         f.write(str(entry["id"]) + ', ' + str(entry["created_at"]) + ', ' + str(entry["public_metrics"]["reply_count"])+'\n')
    
    exit()

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {envBear['BEARER_TOKEN']}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

nasa_tweets2 = "https://api.twitter.com/1.1/search/tweets.json?q="+urllib.parse.quote_plus("#crypto OR #giveaway")+"&result_type=popular&count=50"

reqJson = get_req(fname, nasa_tweets2, debug=False).json()
save_json_to_file(reqJson)

