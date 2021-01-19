import json
import importlib.resources

with importlib.resources.open_text("genderalize", "words.json") as f:
    gendered_dict = json.load(f)