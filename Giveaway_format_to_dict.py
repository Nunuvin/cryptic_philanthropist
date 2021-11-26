import json

GIVEAWAY_FILE_IN = './Outputs/final_giveaways.json'
GIVEAWAY_FILE_OUT = './Outputs/final_giveaways_dict.json'

out_giveaway_dict = {}

with open(GIVEAWAY_FILE_IN, 'r') as infile:
    giveaway_dict = json.load(infile)

    for entry in giveaway_dict:
        out_giveaway_dict[entry['id']] = entry


with open(GIVEAWAY_FILE_OUT, 'w') as outfile:
    outfile.seek(0)
    json.dump(out_giveaway_dict, outfile)
