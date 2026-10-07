import pandas as pd
from sklearn.utils import resample

df = pd.read_csv('data/phishing_emails.csv')

df = df.drop_duplicates()
df = df.dropna(subset=['body', 'label'])

print(df['label'].value_counts())

phishing = df[df['label'] == 1]
legitimate = df[df['label'] == 0]

min_size = min(len(phishing), len(legitimate))
phishing = resample(phishing, n_samples=min_size, random_state=42)
legitimate = resample(legitimate, n_samples=min_size, random_state=42)

df_balanced = pd.concat([phishing, legitimate])
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

df_balanced.to_csv('data/cleaned_emails.csv', index=False)
print("Preprocessing complete. Shape:", df_balanced.shape)