import json
import time
import anthropic

client = anthropic.Anthropic(api_key=)

with open('data/reasoning.json', 'r') as f:
    reasoning_list = json.load(f)

def get_prompt(style, email_text, features, prediction, confidence):
    base = f"""
Email Text: {email_text[:500]}
Classifier Prediction: {'Phishing' if prediction == 1 else 'Legitimate'}
Confidence Score: {confidence:.2f}
Key Features Detected: {', '.join(features)}
"""
    if style == 'technical':
        return base + "Provide a technical explanation using cybersecurity and machine learning terminology explaining why this email was classified as phishing."
    elif style == 'simple':
        return base + "Explain in simple, plain English why this email was flagged as phishing. Avoid technical jargon."
    elif style == 'narrative':
        return base + "Use a relatable story or analogy to explain why this email is suspicious, as if explaining to someone with no technical knowledge."

results = []

for item in reasoning_list:
    row = {'email_id': item['email_id']}
    for style in ['technical', 'simple', 'narrative']:
        prompt = get_prompt(
            style,
            item['email_text'],
            item['top_features'],
            item['prediction'],
            item['confidence']
        )
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            row[style] = response.content[0].text
        except Exception as e:
            row[style] = "Error: " + str(e)
        time.sleep(0.5)
    results.append(row)
    print(f"Generated explanations for email {item['email_id']}")

with open('explanations/all_explanations.json', 'w') as f:
    json.dump(results, f, indent=2)

print("All 900 explanations generated.")