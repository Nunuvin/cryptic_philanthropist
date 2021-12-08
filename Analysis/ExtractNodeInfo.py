import json
import sys

IN_FILE = '../Outputs/final_giveaways_dict.json'

with open(IN_FILE, 'r') as f:
    data = json.load(f)
    print(data[sys.argv[1]])