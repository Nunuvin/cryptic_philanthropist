import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')


FILE_NAME = './Outputs/tweets2.json'


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


# Gets the comments for the specified tweeet, for the specified token. If token is empty, it will not be passed
def getTweetComments(token):
    append_token = ""
    if not(token == None):
        append_token = "&next_token=" + token

    search_url = "https://api.twitter.com/2/tweets/search/recent?query=%23crypto%20%23giveaway%20(tag%20OR%20comment)%20-is%3Aretweet%20-is%3Areply%20-is%3Aquote&tweet.fields=conversation_id,in_reply_to_user_id,author_id,referenced_tweets,source,text,id,public_metrics&expansions=author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&max_results=100{}".format(
        append_token)

    r_josn = requests.get(search_url, auth=bearer_oauth).json()

    return r_josn

# Extracts all the comments from the speicified post, and puts them in a json file


def main():

    next_token_value = None
    data_in = []
    while(True):
        r_json = getTweetComments(next_token_value)

        try:
            next_token_value = r_json["meta"]["next_token"]
            for entry in r_json["data"]:
                data_in.append(entry)

        except KeyError:
            next_token_value = None

        print(next_token_value)

        if(next_token_value == None):
            break



    # Output into the JSON file the new content
    with open(FILE_NAME, 'w') as outfile:
        outfile.seek(0)
        json.dump(data_in, outfile)


# Sample data retrival
main()