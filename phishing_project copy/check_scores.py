import pandas as pd
df = pd.read_csv('evaluation/scores.csv')
print(df.head())
print(df.columns.tolist())