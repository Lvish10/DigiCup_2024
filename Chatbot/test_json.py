import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    try:
        with open(os.path.join(BASE_DIR, filename), 'r') as f:
            data = json.load(f)
            print(f"{filename} loaded successfully")
            return data
    except json.JSONDecodeError as e:
        print(f"Error loading {filename}: {e}")

# Test each JSON file
load_json('fish.json')
load_json('marine_data.json')
load_json('marine_laws.json')
