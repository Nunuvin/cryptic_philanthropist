# By Lior Somin
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')


FILE_NAME = './Outputs/data.json'


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


# Gets the comments for the specified tweeet, for the specified token. If token is empty, it will not be passed
def getTweetComments(post_id, token):
    append_token = ""
    if not(token == None):
        append_token = "&next_token=" + token

    search_url = " https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{}&tweet.fields=in_reply_to_user_id,author_id,created_at,conversation_id&max_results=100{}".format(
        post_id, append_token)

    r_josn = requests.get(search_url, auth=bearer_oauth).json()

    return r_josn

# Extracts all the comments from the speicified post, and puts them in a json file


def extractComments(post_id):

    next_token_value = None
    data_in = []
    while(True):
        r_json = getTweetComments(post_id, next_token_value)

        try:
            next_token_value = r_json["meta"]["next_token"]
            for entry in r_json["data"]:
                data_in.append(entry)

        except KeyError:
            next_token_value = None

        print(next_token_value)

        if(next_token_value == None):
            break

    # Load the JSON file contents
    with open(FILE_NAME, 'r') as infile:
        new_data = json.load(infile)
        new_data[post_id] = data_in

    # Output into the JSON file the new content
    with open(FILE_NAME, 'w') as outfile:
        outfile.seek(0)
        json.dump(new_data, outfile)


# Sample data retrival
extractComments("1446232111795642374")
extractComments("1446890435444723717")