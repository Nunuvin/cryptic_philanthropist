import pandas as pd
import random


def EdgeSwap():
    df = pd.read_csv("../../Gephi/Gephi_Edge_List.csv")
    #df = pd.read_csv("./test_data.csv")

    print('Startind Edge swap')

    all_ids = list(range(0, len(df)))

    new_data = []

    while len(all_ids) > 1:
        rand_i1 = random.randint(0,len(all_ids)-1)
        v1 = all_ids[rand_i1]
        all_ids.pop(rand_i1)

        rand_i2 = random.randint(0,len(all_ids)-1)
        v2 = all_ids[rand_i2]
        all_ids.pop(rand_i2)


        e1 = [df.iloc[v1]['Source'], df.iloc[v2]['Target'], df.iloc[v1]['Weight']]
        e2 = [df.iloc[v2]['Source'], df.iloc[v1]['Target'], df.iloc[v2]['Weight']]

        new_data.append(e1)
        new_data.append(e2)
    
    return new_data