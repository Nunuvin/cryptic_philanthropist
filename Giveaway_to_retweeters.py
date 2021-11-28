# By Lior Somin
import json

IN_FILE_NAME = './Outputs/final_giveaways.json'
OUT_FILE_NAME = './Outputs/post_to_retweeters.json'


def readFromGiveawayFile():

    final_obj = {}
    # Load the JSON file contents
    with open(IN_FILE_NAME, 'r') as infile:

        data_in = json.load(infile)
        for obj in data_in:
            try:
                if obj['referenced_tweets'][0]['type'] == 'retweeted':
                    parent = obj['referenced_tweets'][0]['id']
                    # print(parent)

                    if(not(parent in final_obj)):
                        final_obj[parent] = [obj["author_id"]]
                    else:
                        if(not(obj["author_id"] in final_obj[parent])):
                            final_obj[parent].append(obj["author_id"])
            except KeyError:
                print('got a source! = ' + obj['id'])

    # Here we delete posts that have less than 1 RTs
    posts_to_delete = []
    for post_entry in final_obj:
        if(len(final_obj[post_entry]) < 1):
            posts_to_delete.append(post_entry)

    for post_delete in posts_to_delete:
        final_obj.pop(post_delete)

    with open(OUT_FILE_NAME, 'w') as outfile:
        outfile.seek(0)
        json.dump(final_obj, outfile)

    # Printing # of users
    counter = 0
    for n in final_obj:
        print(n + " ----> " + str(len(final_obj[n])))
        counter = counter + 1

    print("toal = " + str(counter))


readFromGiveawayFile()
