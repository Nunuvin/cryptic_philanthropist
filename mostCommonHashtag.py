import json

INFILE = './Outputs/Community_Hashtags.json'

def countHashtags():
    with open(INFILE) as f:
        data = json.load(f)

    hashtagCount = {}
    for Community, hashtags in data.items():
        #print(Community)
        if Community == '3':
            for hashtag in hashtags:
                if hashtag in hashtagCount:
                    count = hashtagCount[hashtag] + 1
                    #print(count)
                    hashtagCount.update({hashtag: count})
                    #print(hashtagCount)
                else:
                    hashtagCount[hashtag] = 1
    print(hashtagCount)

countHashtags()

