import json
import pandas as pd
import time
import re
import anthropic

client = anthropic.Anthropic(api_key=)

with open('explanations/all_explanations.json', 'r') as f:
    explanations = json.load(f)

with open('data/reasoning.json', 'r') as f:
    reasoning = json.load(f)

reasoning_map = {r['email_id']: r for r in reasoning}

results = []

for item in explanations:
    email_id = item['email_id']
    r = reasoning_map[email_id]
    top_features = r['top_features']
    email_text = r['email_text']

    row = {'email_id': email_id}

    for style in ['technical', 'simple', 'narrative']:
        explanation = item[style]

        # 1. Fidelity Score
        mentioned = sum(1 for f in top_features if f.lower() in explanation.lower())
        fidelity = mentioned / len(top_features) if top_features else 0

        # 2. Readability Score (manual Flesch Kincaid calculation)
        words = len(explanation.split())
        sentences = max(1, len(re.split(r'[.!?]', explanation)))
        syllables = sum(max(1, len(re.findall(r'[aeiouAEIOU]', w))) for w in explanation.split())
        if words > 0:
            readability = round(206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words), 3)
        else:
            readability = 0

        # 3. LLM as Judge Score
        judge_prompt = f"""
You are an expert in cybersecurity and explainable AI.

Original Email: {email_text[:300]}
Model Features Detected: {', '.join(top_features)}
Generated Explanation: {explanation}

Score the explanation from 1 to 5 on each of the following:
- accuracy: does it correctly describe why this is phishing?
- clarity: is it easy to understand?
- completeness: does it cover the key phishing indicators?

Return ONLY a JSON object like this with no extra text:
{{"accuracy": 4, "clarity": 3, "completeness": 4}}
"""
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=150,
                messages=[{"role": "user", "content": judge_prompt}]
            )
            raw = response.content[0].text.strip()
            # Extract JSON even if there is extra text around it
            json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
            else:
                print(f"No JSON found for email {email_id} style {style}, raw: {raw}")
                scores = {"accuracy": 0, "clarity": 0, "completeness": 0}
        except Exception as e:
            print(f"Judge error for email {email_id} style {style}: {e}")
            scores = {"accuracy": 0, "clarity": 0, "completeness": 0}

        time.sleep(1)

        row[f'{style}_fidelity'] = round(fidelity, 3)
        row[f'{style}_readability'] = round(readability, 3)
        row[f'{style}_accuracy'] = scores.get('accuracy', 0)
        row[f'{style}_clarity'] = scores.get('clarity', 0)
        row[f'{style}_completeness'] = scores.get('completeness', 0)

    results.append(row)
    print(f"Evaluated email {email_id}")

df = pd.DataFrame(results)
df.to_csv('evaluation/scores.csv', index=False)
print("Evaluation complete. Scores saved.")