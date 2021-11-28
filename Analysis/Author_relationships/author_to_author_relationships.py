# does the following:
# import author info from giveaway_tweets_info.json
# add info about what community they are from, from csv thing
# use the finals_giveaway.json to get the author relationships (do authors retweet each other) [weighted graph]
## figure if this is a retweet. if so get the author and figure who they retweeted
# prob viz this
# does this align with communities?
# who is the most retweeted author?

import json
import csv

GIVEAWAYTWEETS = "../../Outputs/Giveaway_tweets_info.json"
GEPHY_NODES_LIST_COMM = "../../Gephi/Gephi_Nodes_List.csv"
ALL_POSTS = "../../Outputs/final_giveaways.json"

GEPHY_AUTHOR_EDGE_LIST = "../../Gephi/Authors/Gephi_Author_Edge_List.csv"
GEPHY_AUTHOR_NODES_LIST = "../../Gephi/Authors/Gephi_Author_Nodes_List.csv"

def read_gephy_comm_csv(filename):
    postToComm = {}
    with open(filename, newline='') as csvf:
        gephyReader = csv.reader(csvf, delimiter=',')
        for row in gephyReader:
            postToComm[row[1]] = row[4]
    return postToComm

def read_json_from_file(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        #print(f.readline())
        return data

def posts_to_author(posts):
    authorPosts = {}
    for postId, postData in posts.items():
        if postData["author_id"] in authorPosts:
            authorPosts[postData["author_id"]].append(postId)
        else:
            authorPosts[postData["author_id"]]=[postId]
    return authorPosts

def author_to_posts(posts):
    postsIds = {}
    for postId, postData in posts.items():
        postsIds[postId] = postData["author_id"]
    return postsIds


def who_reposted_who(posts, postsToAuthor):
    reposterToPoster = {}
    posterToReposter = {}
    for post in posts:
        #print(post)
        if "referenced_tweets" in post:
            if post["referenced_tweets"][0]["type"] == "retweeted":
                #if it was a retweet; get author info
                authorId = post["author_id"]
                refTweetId = post["referenced_tweets"][0]["id"]
                try:
                    refTweetAuthor = postsToAuthor[refTweetId]
                except Exception as e:
                    pass #1k nodes have no author info due to it being deleted from twitter
                
                if authorId in reposterToPoster:
                    reposterToPoster[authorId].append(refTweetAuthor)
                else:
                    reposterToPoster[authorId]= [refTweetAuthor]

                if refTweetAuthor in posterToReposter:
                    posterToReposter[refTweetAuthor].append(authorId)
                else:
                    posterToReposter[refTweetAuthor] = [authorId]
    return reposterToPoster, posterToReposter

def author_to_comm(authorToPosts, postsToComm):
    authors = authorToPosts.keys()
    authorToComms = {}
    for author in authors:
        for post in authorToPosts[author]:
            comm = postsToComm[post]
            if author in authorToComms:
                authorToComms[author].add(comm)
            else:
                authorToComms[author] = set(comm)
    return authorToComms

def print_x_to_y(authorPosts):
    for author in authorPosts:
        print(author," : ",authorPosts[author])

def export_gephi_author_node_list(reposterToPoster, posterToReposter):
    global GEPHY_AUTHOR_NODES_LIST
    authorToId = {}
    with open(GEPHY_AUTHOR_NODES_LIST, 'w', newline='') as csvf:
        nodeWriter = csv.writer(csvf, delimiter=',')
        nodeWriter.writerow(["Id", "Label", "timeset", "size"]) #header

        authors = posterToReposter.keys()
        for i, author in enumerate(authors):
            #print(i, author)
            authorToId[author] = i
            nodeWriter.writerow([i,author,"",len(posterToReposter[author])])
    return authorToId

def export_gephi_author_edge_list(reposterToPoster, posterToReposter, authorToId):
    global GEPHY_AUTHOR_EDGE_LIST
    authors = posterToReposter.keys()
    with open(GEPHY_AUTHOR_EDGE_LIST, 'w', newline='') as csvf:
        edgeWriter = csv.writer(csvf, delimiter=',')
        edgeWriter.writerow(["Source", "Target", "Type", "Id", "Label", "timeset", "Weight"]) # header
        #note this is a directed graph
        i=0
        for author in authors:
            srcId = authorToId[author]
            if author in reposterToPoster:
                posters = reposterToPoster[author] #list
                for poster in posters:
                    if poster in authorToId:
                        targetId = authorToId[poster]
                        weight = posters.count(poster)
                        edgeWriter.writerow([srcId, targetId, "directed", i, "", "", weight])
                        i += 1
    

def export_to_gephi_format(reposterToPoster, posterToReposter): 
    authorToId = export_gephi_author_node_list(reposterToPoster, posterToReposter)
    export_gephi_author_edge_list(reposterToPoster, posterToReposter, authorToId)

def main():
    global GIVEAWAYTWEETS
    global GEPHY_NODES_LIST_COMM
    global ALL_POSTS

    unique_posts = read_json_from_file(GIVEAWAYTWEETS) #json which is now a dict, has uniq posts
    all_posts = read_json_from_file(ALL_POSTS)

    #hashtables for lookups
    postToComm = read_gephy_comm_csv(GEPHY_NODES_LIST_COMM)
    
    authorToPosts = posts_to_author(unique_posts) # grouped posts to author.
    postsToAuthor = author_to_posts(unique_posts) # get author to post
    
    authorToComms = author_to_comm(authorToPosts, postToComm)
    #!!!!!
    reposterToPoster, posterToReposter = who_reposted_who(all_posts, postsToAuthor) # just author data of who reposted who
    #!!!!!

    export_to_gephi_format(reposterToPoster, posterToReposter)

    #print_x_to_y(reposterToPoster)


if __name__ == "__main__":
    main()