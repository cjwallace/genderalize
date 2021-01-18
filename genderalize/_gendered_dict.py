import json

with open("genderalize/words.json", "r") as f:
    raw_json = f.read()

gendered_dict = json.loads(raw_json)