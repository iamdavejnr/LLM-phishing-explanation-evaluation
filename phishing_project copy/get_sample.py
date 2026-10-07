import json

with open('explanations/all_explanations.json', 'r') as f:
    explanations = json.load(f)

with open('data/reasoning.json', 'r') as f:
    reasoning = json.load(f)

# Get first email as example
email = explanations[0]
reason = reasoning[0]

print("EMAIL TEXT:")
print(reason['email_text'][:300])
print("\nTECHNICAL EXPLANATION:")
print(email['technical'])
print("\nSIMPLE EXPLANATION:")
print(email['simple'])
print("\nNARRATIVE EXPLANATION:")
print(email['narrative'])