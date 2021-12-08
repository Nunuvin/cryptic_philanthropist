import json
import datetime

path_avg = 0
clustering_avg = 0
closeness_avg = 0
Delta_time_avg = 0

for i in range(0,100):
    with open('./DataStats/Null_Model_'+str(i)+".json", 'r') as f:
        data = json.load(f)
        path_avg += data['path'][0]
        Delta_time_avg += data['Delta_time']
        closeness_avg += data['closeness']
        clustering_avg += data['clustering']

path_avg /= 100
clustering_avg /= 100
closeness_avg /= 100
Delta_time_avg /= 100

print("path = " + str(path_avg))
print("clustering = " + str(clustering_avg))
print("closeness = " + str(closeness_avg))
print("Delta_time_ = " + str(datetime.timedelta(seconds=Delta_time_avg)))
