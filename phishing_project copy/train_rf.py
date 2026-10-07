import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

df = pd.read_csv('data/cleaned_emails.csv')

# Use 'body' instead of 'text'
X = df['body'].fillna('')
y = df['label']

vectorizer = TfidfVectorizer(max_features=3000)
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, stratify=y, random_state=42
)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

pickle.dump(rf, open('models/rf_model.pkl', 'wb'))
pickle.dump(vectorizer, open('models/vectorizer.pkl', 'wb'))

# Save test set indices
test_indices = y_test.index
df_test = df.iloc[test_indices].copy()
df_test.to_csv('data/test_set.csv', index=False)
print("Model and test set saved.")