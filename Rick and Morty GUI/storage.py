import json
import os
from datetime import datetime

# через этот файл сохраняются и загружаются данные энциклопедии и история действий пользователя

ENCYCLOPEDIA_FILE = "encyclopedia.json"
HISTORY_FILE = "history.json"

def load_encyclopedia():
    if os.path.exists(ENCYCLOPEDIA_FILE):
        with open(ENCYCLOPEDIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_encyclopedia(data):
    with open(ENCYCLOPEDIA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_to_history(action):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append({"time": str(datetime.now())[:19], "action": action})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []