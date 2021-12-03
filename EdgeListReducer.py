import pandas as pd

df = pd.read_csv('./Gephi/Gephi_Edge_List.csv')

df_out = df.loc[df['Weight'] > 4]

df_out.to_csv('./Gephi/Gephi_Edge_List_FILTERED.csv')
