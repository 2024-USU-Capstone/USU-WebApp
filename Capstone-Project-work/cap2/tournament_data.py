# tournament_data.py
import json
import os

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, 'tournaments.json')

def load_tournaments():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create it with empty list
        save_tournaments([])
        return []

def save_tournaments(tournaments):
    with open(JSON_FILE, 'w') as file:
        json.dump(tournaments, file, indent=2)

def add_tournament(tournament):
    tournaments = load_tournaments()
    tournaments.append(tournament)
    save_tournaments(tournaments)

def delete_tournament(tournament_id):
    tournaments = load_tournaments()
    tournaments = [t for t in tournaments if t['id'] != tournament_id]
    save_tournaments(tournaments)