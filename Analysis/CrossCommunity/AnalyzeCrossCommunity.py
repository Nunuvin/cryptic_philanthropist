import json
import pandas as pd
from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


cross_community_list = {}

with open('./Node_to_community.json', 'r') as f:
    cross_community_list = json.load(f)

overlapped_communities = {}

overlapped_nodes = {}

# Get the most overlapped community
for entry in cross_community_list:

    mod_class = cross_community_list[entry]["Original"]

    if mod_class not in overlapped_communities:
        overlapped_communities[mod_class] = 1
    else:
        overlapped_communities[mod_class] = overlapped_communities[mod_class] + 1


df = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)

print(len(df[df['modularity_class'] == '4']))

# Get the most overlapping nodes
for entry in cross_community_list:

    overlapped_nodes[entry] = len(
        cross_community_list[entry]["Target modularity"])

print(' ------ MOST OVERLAPPING COMMUNITIES ------')
sorted_overlapped_communities = dict(sorted(overlapped_communities.items(),
                                            key=lambda item: item[1], reverse=True))

iterator = iter(sorted_overlapped_communities.items())
for i in range(10):
    val = next(iterator)
    print(val[0] + ": " + str(val[1]) + "/" +
          str(len(df[df['modularity_class'] == val[0]])))

print(' ------ MOST OVERLAPPING NODES ------')
sorted_overlapped_nodes = dict(sorted(overlapped_nodes.items(),
                                      key=lambda item: item[1], reverse=True))

iterator = iter(sorted_overlapped_nodes.items())
for i in range(10):
    print(next(iterator))
