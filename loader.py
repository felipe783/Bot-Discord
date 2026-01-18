import json
import os

def load_db():
    if os.path.exists("Json/Data.json"):
        with open("Json/Data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_db(dados):
    with open("Json/Data.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

