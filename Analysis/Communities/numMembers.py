import pandas as pd

df = pd.read_csv("../../Gephi/Gephi_Nodes_List.csv")

print(len(df.loc[df['modularity_class'] == 146]))