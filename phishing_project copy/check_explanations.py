import json

with open('explanations/all_explanations.json', 'r') as f:
    data = json.load(f)

print(data[0])