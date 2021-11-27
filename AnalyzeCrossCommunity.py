import json

cross_community_list = {}

with open('./Gephi/Node_to_community.json', 'r') as f:
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


print(overlapped_communities)

# Get the most overlapping nodes
for entry in cross_community_list:

    overlapped_nodes[entry] = len(
        cross_community_list[entry]["Target modularity"])


print(overlapped_communities)
print(overlapped_nodes)
