import pandas as pd
df = pd.read_csv('data/cleaned_emails.csv')
print(df.columns.tolist())
print(df.head())