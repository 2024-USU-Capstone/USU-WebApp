# tournament_data.py
import json
import os
import math
from flask import jsonify
from datetime import datetime
# Get the directory where the script is located
#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#JSON_FILE = os.path.join(SCRIPT_DIR, 'tournaments.json')
import logging
import random

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG for detailed information)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
)

logger = logging.getLogger(__name__)  # Get a logger for this module

def load_tournaments(mydb):    #converts to 12hr format
    cursor = mydb.cursor()
    insert_query = """
        SELECT * from Tournaments
    """
    cursor.execute(insert_query)
    return [
        {
            'id': row[0],
            'name': row[1],
            'date': row[2],
            'start_time': (datetime(1, 1, 1) + row[3]).strftime('%I:%M %p'),
            'end_time': (datetime(1, 1, 1) + row[4]).strftime('%I:%M %p'), 
            'type': row[5],
            'location': row[6]
        }
        for row in cursor.fetchall()
    ]    #return list of dictionarys mapped to tournament database element 

def load_tournament_students(mydb):
    cursor = mydb.cursor()
    cursor.execute("""
        SELECT tt.tournament_id, tm.student_id, tm.team_id, s.fname, s.lname, t.team_name
        FROM Tournament_teams tt
        JOIN Team_members tm ON tt.team_id = tm.team_id
        JOIN Students s ON tm.student_id = s.student_id
        JOIN Teams t ON tm.team_id = t.team_id
    """)
    return [{'tournament_id': row[0], 'student_id': row[1], 'team_id': row[2], 'name': f"{row[3]} {row[4]}", 'team_name': row[5]} for row in cursor.fetchall()]

    
def insert_team(mydb, student):
    cursor = mydb.cursor()
    
    cursor.execute("INSERT INTO Teams (team_name) VALUES (%s)", (student['team_name'],))
    mydb.commit()
    team_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM Team_members tm  WHERE tm.student_id = %s AND tm.team_id = %s", (student["studentid"], team_id))
    student_in_team = cursor.fetchall()
    logger.debug("Student_in_team==")
    logger.debug(student_in_team)
    logger.debug("\n")
    logger.debug("team_id==")
    logger.debug(team_id)
    logger.debug("\n")
    logger.debug("studentid==")
    logger.debug(student["studentid"])
    logger.debug("\n")
    if len(student_in_team) == 0:
        cursor.execute("INSERT INTO Team_members (student_id, team_id) VALUES (%s, %s)", (student['studentid'], team_id))
        mydb.commit()

    cursor.close()
    return team_id
    


def register_student(mydb, student):
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student['studentid'],))
    existing_student = cursor.fetchone();
    if not existing_student:
        insert_student = "INSERT INTO Students (student_id, fname, lname, last_checked_out) VALUES (%s, %s, %s, NOW())"
        cursor.execute(insert_student, (student['studentid'], student['fname'], student['lname']))
        mydb.commit()    
    
    team_id = insert_team(mydb, student) #See insert_team function above
    
    insert_tournament_team = "INSERT INTO Tournament_teams (tournament_id, team_id) VALUES (%s, %s)"
    cursor.execute(insert_tournament_team, (student['tournament_id'], team_id))
    mydb.commit()
    
    cursor.close()


def insert_tournament(mydb, tournament):
    cursor = mydb.cursor()
    insert_query = """
        INSERT into Tournaments (tournament_name, tournament_date, tournament_start, tournament_end, tournament_location, tournament_type, team_based)
        values (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        tournament['name'],
        tournament['date'],
        tournament['start_time'],
        tournament['end_time'],
        tournament['location'],
        tournament['type'],
        1 if tournament['team_based'] == 'TRUE' else 0 #Note team_based is boolean which is converted to 1 or 0 for SQL storage
    ))
    mydb.commit()
    print(f"Tournament '{tournament['name']}' added successfully with ID: {cursor.lastrowid}")


def delete_tournament(mydb, tournament_id):
    cursor = mydb.cursor()
    delete_query = """
        DELETE from Tournaments
        WHERE tournament_id = %s;
    """
    cursor.execute(delete_query, (tournament_id,)) #Second param must be tuple
    mydb.commit()


def select_matches(mydb, tournament_id):
    cursor = mydb.cursor() 
    cursor.execute("SELECT * FROM Matches WHERE tournament_id = %s", (tournament_id,))
    matches_data = cursor.fetchall()
    
    cursor.execute("""
        SELECT tt.team_id, t.team_name, s.fname
        FROM Tournament_teams tt
        JOIN Teams t ON tt.team_id = t.team_id
        JOIN Team_members tm ON tt.team_id = tm.team_id
        JOIN Students s ON tm.student_id = s.student_id
        WHERE tt.tournament_id = %s;
    """, (tournament_id,))
    team_members_data = cursor.fetchall()
    team_names = {}
    team_members = {}

    for team_id, team_name, fname in team_members_data:
        team_names[team_id] = team_name
        if team_id not in team_members:
            team_members[team_id] = []
        team_members[team_id].append(fname)
        
    matches = [{
        'match_id': row[0],
        'tournament_id': row[1],
        'round_number': row[2],
        'team_a_id': row[3],
        'team_a_name': team_names.get(row[3]),  
        'team_a_members': team_members.get(row[3], []),  
        'team_b_id': row[4],
        'team_b_name': team_names.get(row[4]), 
        'team_b_members': team_members.get(row[4], []),  
        'player_a_score': row[5],
        'player_b_score': row[6],
        'match_winner': row[7],
        'status': row[8]
    } for row in matches_data]
    return jsonify(matches)

#####################################
#### TOURNAMENT BRACKET CREATION ####
#####################################

def create_bracket_single_elim(mydb, tournament_id):
    cursor = mydb.cursor() 
    cursor.execute(
        "SELECT t.* FROM Teams t "
        "JOIN Tournament_teams tt ON t.team_id = tt.team_id "
        "JOIN Tournaments tr ON tt.tournament_id = tr.tournament_id "
        "WHERE tr.tournament_id = %s", (tournament_id,)
    )
    teams = [{'team_id': row[0], 'team_name': row[1]} for row in cursor.fetchall()]
    random.shuffle(teams)  # Randomizes the order of teams
    team_count = len(teams)
    round_count = math.ceil(math.log2(team_count)) #
    
    
    if team_count < 2:
        return {"error": "At least 2 teams are required to create a bracket."}

    matches = []
    for round_number in range(1, round_count + 1):
        for i in range(0, team_count, 2):
            match = {
                'tournament_id': tournament_id,
                'round_number': round_number,
                'team_a_id': teams[i]['team_id'] if i < team_count and round_number == 1 else None,
                'team_b_id': teams[i + 1]['team_id'] if i + 1 < team_count and  round_number == 1 else None,
                'status': 'pending'
            }
            matches.append(match)
        team_count = math.ceil(team_count / 2)

    insert_query = """
    INSERT INTO Matches (tournament_id, round_number, team_a_id, team_b_id, status)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        for match in matches:
            cursor.execute(insert_query, (
                match['tournament_id'],
                match['round_number'],
                match['team_a_id'],
                match['team_b_id'],
                match['status']
            ))
        mydb.commit()
        return len(matches)
    except Exception as e:
        print(f"Error inserting matches: {e}")
        mydb.rollback()  # Rollback if there was an error
        return None  # Return None to indicate failure

def selectwinner(mydb, tournament_id, match_data):
    cursor = mydb.cursor() 
    update_query = """
    UPDATE Matches
    SET
        player_a_score = %s,
        player_b_score = %s,
        match_winner = %s,
        status = 'completed'
    WHERE
        match_id = %s AND tournament_id = %s
    """
    score_a = match_data['score_a']
    score_b = match_data['score_b']
    winner_id = match_data['winner_id']
    match_id = match_data['match_id']
    match_round = match_data['match_round']
    cursor.execute(update_query, (score_a, score_b, winner_id, match_id, tournament_id))
    mydb.commit()

    next_round = int(match_round) + 1
    next_round_query = """
        SELECT match_id, team_a_id, team_b_id FROM Matches
        WHERE tournament_id = %s AND round_number = %s
        AND (team_a_id IS NULL OR team_b_id IS NULL)
    """
    cursor.execute(next_round_query, (tournament_id, next_round))
    next_round_matches = cursor.fetchall()

    if next_round_matches:
        random_match = random.choice(next_round_matches)  # Select a random match
        random_match_id = random_match[0]
        random_match_teama = random_match[1]
        random_match_teamb = random_match[2]
        if random_match_teama is None:
            # Insert the winner in team_a_id if it's empty
            update_next_round_query = """
            UPDATE Matches
            SET team_a_id = %s
            WHERE match_id = %s
            """
            cursor.execute(update_next_round_query, (winner_id, random_match_id))
        elif random_match_teamb is None:
            # Insert the winner in team_b_id if it's empty
            update_next_round_query = """
            UPDATE Matches
            SET team_b_id = %s
            WHERE match_id = %s
            """
            cursor.execute(update_next_round_query, (winner_id, random_match_id))

        mydb.commit()

    return

def create_bracket_round_robin():
    pass

def create_bracket_swiss():
    pass

def create_bracket_round_robin():
    pass

#cursor.execute("SELECT tt.team_id, t.team_name FROM Tournament_teams tt JOIN Teams t ON tt.team_id = t.team_id WHERE tt.tournament_id = %s;", (tournamentid,))
    #teams_data = cursor.fetchall()
    #team_names = {row[0]: row[1] for row in teams_data} #dictionary of {teamid: teamname}