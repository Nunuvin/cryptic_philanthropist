import csv
import json 
from datetime import datetime, timedelta
from dateutil import parser as dateParser

TOP100EDGE = "../../Outputs/top100Edgelist.csv"
NODELIST = "../../Outputs/NodeList.csv"
GIVEAWAYTWEETS = "../../Outputs/Giveaway_tweets_info.json"

def read_json_from_file(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        #print(f.readline())
        return data

def read_aliased_top_edges():
    with open(TOP100EDGE, newline='') as f:
        csvreader = csv.reader(f, delimiter=',')
        ls = {}
        for line in csvreader:
            d = {}
            d["source"] = line[0]
            d["target"] = line[1]
            d["weight"] = line[2]
            ls[(d["source"], d["target"])] = d
        return ls

def read_nodelist():
    with open(NODELIST, newline='') as f:
        csvreader = csv.reader(f, delimiter=',')
        ls = {}
        for line in csvreader:
            d = {}
            d["id"] = line[0]
            d["label"] = line[1]
            d["size"] = line[2]
            ls[d["id"]] = d
        return ls


def top_nodes(topEdges, nodeToTweet):
    ls = []
    for edge in topEdges:
        node1 = nodeToTweet[edge[0]]["label"]
        node2 = nodeToTweet[edge[1]]["label"]
        ls.append((node1, node2, int(topEdges[edge]["weight"])))
    return sorted(ls, key=lambda tup: tup[2], reverse=True)

def compute_time_diff(nodePair, posts):
    if nodePair[0] in posts and nodePair[1] in posts:
        # print(posts[nodePair[0]]['created_at'])
        # print(posts[nodePair[1]]['created_at'])
        dt1 = dateParser.isoparse(posts[nodePair[0]]['created_at'])
        dt2 = dateParser.isoparse(posts[nodePair[1]]['created_at'])
        # print(dt1-dt2)
        return dt1 - dt2, 1
    return None, 0

def compute_avg_time_diff(nodePairs, posts):
    dx = timedelta()
    ctr = 0
    for nodePair in nodePairs:
        ddx, cctr = compute_time_diff(nodePair, posts)
        if ddx is not None:
            dx += ddx
            ctr += cctr
    print("validTweetPairs:", ctr)
    return dx/ctr

def main():
    top100Edges = read_aliased_top_edges()
    nodeToTweet = read_nodelist()
    nodePairs = top_nodes(top100Edges, nodeToTweet)
    # print(nodePairs)
    # nodepair source -> target weight

    posts = read_json_from_file(GIVEAWAYTWEETS)
    #print(posts)
    avgTimediff = compute_avg_time_diff(nodePairs, posts)
    print(avgTimediff)

if __name__ == "__main__":
    main()