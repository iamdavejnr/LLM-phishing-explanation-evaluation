import pandas as pd
import pickle
import shap
import json
import numpy as np

rf = pickle.load(open('models/rf_model.pkl', 'rb'))
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))

df = pd.read_csv('data/test_set.csv')

sample = df.sample(n=300, random_state=42).reset_index(drop=True)

# Convert sparse matrix to dense array to fix SHAP compatibility issue
X_sample = vectorizer.transform(sample['body'].fillna(''))
X_sample_dense = X_sample.toarray().astype(float)

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_sample_dense, check_additivity=False)
feature_names = vectorizer.get_feature_names_out()
reasoning_list = []

for i in range(len(sample)):
    shap_vals = shap_values[1][i]
    top_indices = shap_vals.argsort()[-3:][::-1]
    top_features = [feature_names[j] for j in top_indices]
    reasoning_list.append({
        'email_id': i,
        'email_text': sample['body'][i],
        'label': int(sample['label'][i]),
        'prediction': int(rf.predict(X_sample_dense[i].reshape(1, -1))[0]),
        'confidence': float(rf.predict_proba(X_sample_dense[i].reshape(1, -1))[0][1]),
        'top_features': top_features
    })

with open('data/reasoning.json', 'w') as f:
    json.dump(reasoning_list, f, indent=2)

print("SHAP reasoning extracted for 300 emails.")