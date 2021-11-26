import json
from dotenv import load_dotenv
import os
import time
import requests

# GLOBALS
load_dotenv()
envBear = {}
envBear['BEARER_TOKEN'] = os.getenv('BEARER_TOKEN')

GIVEAWAY_FILE_IN = './Outputs/post_to_retweeters.json'
DELETED_TWEETS = "./Outputs/deleted_tweets.json"
PARENT_TWEET_AUTHORS = "./Outputs/Giveaway_tweets_info.json"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {envBear['BEARER_TOKEN']}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def get_tweet_info(ids, i, j):
    id = ""

    while i < j:
        id = id + ids[i] + ","
        i = i + 1

    id = id[:-1]

    url = "https://api.twitter.com/2/tweets?ids=" + id + \
        "&tweet.fields=entities,conversation_id,in_reply_to_user_id,author_id,source,text,id,public_metrics,created_at,geo,referenced_tweets,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    return requests.get(url, auth=bearer_oauth)


def get_parent_tweets():
    global GIVEAWAY_FILE_IN

    out = []

    with open(GIVEAWAY_FILE_IN, 'r') as infile:
        giveaway_dict = json.load(infile)

    for key in giveaway_dict:
        out.append(key)

    out = list(dict.fromkeys(out))
    return out


def main():

    parents = get_parent_tweets()

    print(len(parents))
    i = 0

    parent_data = {}
    error_data = []

    while i < len(parents):
        sub_arr = []
        recieved = []
        if(i+100 > len(parents)):
            r = get_tweet_info(parents, i, len(parents))
            sub_arr = parents[i:len(parents)]
        else:
            r = get_tweet_info(parents, i, i+100)
            sub_arr = parents[i:i+100]

        for obj in r.json()['data']:
            parent_data[obj['id']] = obj
            recieved.append(obj['id'])

        error_data = error_data + list(set(sub_arr) - set(recieved))

        i = i + 100

    with open(DELETED_TWEETS, "w+") as dellog:
        json.dump(error_data, dellog)

    with open(PARENT_TWEET_AUTHORS, "w+") as data:
        json.dump(parent_data, data)


if __name__ == "__main__":
    main()
