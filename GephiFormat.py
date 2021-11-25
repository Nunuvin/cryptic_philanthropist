import json
import csv

# opens json file to read


def readKeyValues(inputJsonFile):
    with open(inputJsonFile, 'r') as infile:
        return json.load(infile)


# print keys = node list
def nodes(dict, NodeOutput):
    header = ['ID', 'Label', 'Size']
    with open(NodeOutput, 'w',  newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    count = 0
    for key in dict:
        #print("ID: " + str(count) + " Label: " + key)
        fields = [count, key, len(dict[key])]
        with open(NodeOutput, 'a',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        count += 1

# edge lists
# loop through author ids and fine common commentors and count


def edges(dict, EdgeOutput):

    header = ['Source', 'Target', 'Weight']
    with open(EdgeOutput, 'w',  newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    retweet_list = list(dict.values())
    # print(retweet_list)
    for i in range(0, len(retweet_list)):
        for j in range(i + 1, len(retweet_list)):
            all_occurrences = (intersection(retweet_list[i], retweet_list[j]))
            if (len(all_occurrences) > 0):
                fields = [i, j, len(all_occurrences)]
                with open(EdgeOutput, 'a',  newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# default values
inputJsonFile = './Outputs/post_to_retweeters.json'

EdgeOutput = './Outputs/EdgeList.csv'

NodeOutput = './Outputs/NodeList.csv'

dict = readKeyValues(inputJsonFile)

nodes(dict, NodeOutput)

edges(dict, EdgeOutput)
