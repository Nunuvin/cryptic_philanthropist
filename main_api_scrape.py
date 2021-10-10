import requests
import json

envBear = {}
saveFiles = {
    "giveawayTweets" : "giveaway.json"
}

searchFollowupUrl = " https://api.twitter.com/2/tweets/search/recent?query=conversation_id:1445052091051876352&tweet.fields=in_reply_to_user_id,author_id,created_at,conversation_id&max_results=100&next_token=b26v89c19zqg8o3fpds84kv5lha4omoyjy3qvfhohy64d"




def load_bearer_token():
    '''
    Reads .bear file and writes data into env dictionary
    .bear Format:
    bearer_token = TOKENVALUE
    '''
    global envBear
    with open(".bear","r") as f:
        lines = f.readlines()
        for l in lines[1:]:
            l = l.split(" ")
            envBear[l[0]] = l[2]
        #print(envBear)

def scrape_giveaways():
    '''
    Get those sweet giveaways
    '''
    global saveFiles

    tweetsByHashtag = "https://api.twitter.com/2/tweets/search/recent?query=%23crypto%20%23giveaway%20(tag%20OR%20comment)%20-is%3Aretweet%20-is%3Areply%20-is%3Aquote&tweet.fields=conversation_id,in_reply_to_user_id,author_id,referenced_tweets,source,text,id,public_metrics&expansions=author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&max_results=100"

    # nasa_tweets = 'https://api.twitter.com/1.1/search/tweets.json?q=crypto%20giveaway&result_type=popular&since_id=1417454251299819520&count=15'
    # nasa_tweets2 = "https://api.twitter.com/1.1/search/tweets.json?max_id=1446475489359585283&q=nasa&include_entities=1&result_type=popular"
    get_req(saveFiles["giveawayTweets"], tweetsByHashtag, debug=False)

def main():
    load_bearer_token() #load env vals
    scrape_giveaways()




def get_req(outputFilename, reqUrl, debug=False):
    r = requests.get(reqUrl, auth=bearer_oauth)
    if debug == False:
        with open(outputFilename, 'w') as outfile:
            json.dump(r.json(), outfile)
    else:
        print(r.json())



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {envBear['bearer_token']}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

if __name__ == "__main__":
    main()