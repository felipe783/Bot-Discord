import json
import os

def load_db():
    if os.path.exists("Data-Base/Data.json"):
        with open("Data-Base/Data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_db(dados):
    with open("Data-Base/Data.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


"""
from datetime import datetime, timedelta
from pathlib import Path
ARQUIVO = Path("Data-Base/Data.json")
def load_db():
    if not ARQUIVO.exists():
        return {
            "historia": [],
            "last_reset": datetime.now().strftime("%Y-%m-%d")
        }

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        db = json.load(f)

    hoje = datetime.now()
    ultimo_reset = datetime.strptime(db["last_reset"], "%Y-%m-%d")

    if hoje - ultimo_reset >= timedelta(days=1):
        # limpa tudo 🔥
        verificação = True
        db["historia"] = []
        db["last_reset"] = hoje.strftime("%Y-%m-%d")

        salvar_db(db)

    return db
"""    