import json
import pandas as pd
from collections import Counter

data = {}
with open('../../Outputs/Giveaway_tweets_info.json', 'r') as f:
    data = json.load(f)

author_to_post = {}

for entry in data:
    if data[entry]['author_id'] in author_to_post:
        author_to_post[data[entry]['author_id']].append(entry)
    else:
        author_to_post[data[entry]['author_id']] = [entry]


with open('./authors_to_posts.json', 'w+') as f:
    json.dump(author_to_post, f)


author_com_freq = {}
df_authors = pd.read_csv('../../Gephi/Authors/authors_nodes.csv', dtype=str)

df_posts = pd.read_csv('../../Gephi/Gephi_Nodes_List.csv', dtype=str)

for index, row in df_authors.iterrows():
    mod_class = row['modularity_class']

    coms = {}
    # Get communities for author
    for post in author_to_post[row['Label']]:
        post_mod = (df_posts.loc[df_posts['Label'] ==
                    post]).iloc[0]['modularity_class']

        if post_mod in coms:
            coms[post_mod] = coms[post_mod] + 1
        else:
            coms[post_mod] = 1

    if mod_class in author_com_freq:
        author_com_freq[mod_class] = dict(
            Counter(author_com_freq[mod_class]) + Counter(coms))
    else:
        author_com_freq[mod_class] = coms


with open('./authors_coms_to_post_coms.json', 'w+') as f:
    json.dump(author_com_freq, f)
