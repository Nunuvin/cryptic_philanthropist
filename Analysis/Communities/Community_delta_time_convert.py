import json
import datetime

with open('./Community_to_delta_time.json', 'r') as f:
    in_data = json.load(f)

out_data = {}
for entry in in_data:
    out_data[entry] = str(datetime.timedelta(seconds=(in_data[entry][0]/in_data[entry][1])))

with open('./Community_to_time.json' , 'w+') as f:
    json.dump(out_data, f)