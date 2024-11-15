# tournament_data.py
import json
import os

# Get the directory where the script is located
#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#JSON_FILE = os.path.join(SCRIPT_DIR, 'tournaments.json')

def load_tournaments():
    pass

def save_tournaments(tournaments):
    pass

def insert_tournament(cursor, tournament):
    insert_query = """
        INSERT into Tournaments (tournament_id, tournament_name, tournament_date, tournament_start, tournament_end, tournament_location)
        values (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        tournament['id'],
        tournament['name'],
        tournament['date'],
        tournament['start_time'],
        tournament['end_time'],
        tournament['location']
    ))

    print(f"Tournament '{tournament['name']}' added successfully with ID: {tournament['id']}")


def delete_tournament(tournament_id):
    pass