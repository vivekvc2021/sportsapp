import sqlite3
import pandas as pd

DATABASE = 'sports_management.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Create tables from schema.sql
def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
        conn.commit()

# Get all teams from the database
def get_teams():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Teams")
        return cursor.fetchall()

# Get all locations from the database
def get_locations():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, stadium_name FROM Locations")
        return cursor.fetchall()

# Add a new team
def add_team(name, coach):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Teams (name, coach) VALUES (?, ?)", (name, coach))
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

# Add a new location
def add_location(stadium_name, city):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Locations (stadium_name, city) VALUES (?, ?)", (stadium_name, city))
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

# Add a new player
def add_player(name, team_id, position):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Players (name, team_id, position) VALUES (?, ?, ?)", (name, team_id, position))
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

# Insert a game
def insert_game(team1_id, team2_id, location_id, date, team1_score, team2_score):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Games (team1_id, team2_id, location_id, date, team1_score, team2_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (team1_id, team2_id, location_id, date, team1_score, team2_score))
        conn.commit()

# Delete a game by ID
def delete_game(game_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Games WHERE id = ?", (game_id,))
        conn.commit()

# Generate game report
def generate_game_report(location_id, start_date, end_date):
    query = """
        SELECT team1_id, team2_id, team1_score, team2_score, date
        FROM Games
        WHERE date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    if location_id:
        query += " AND location_id = ?"
        params.append(location_id)

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()

    report = []
    for game in results:
        report.append({
            "team1": get_team_name(game[0]),
            "team2": get_team_name(game[1]),
            "score": f"{game[2]} - {game[3]}",
            "date": game[4]
        })
    return report

def get_team_name(team_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Teams WHERE id = ?", (team_id,))
        return cursor.fetchone()[0]

def fetch_report_data(start_date, end_date, location, team):
    query = """
        SELECT g.date, t1.name AS team1, t2.name AS team2, g.team1_score, g.team2_score, l.stadium_name
        FROM Games g
        JOIN Teams t1 ON g.team1_id = t1.id
        JOIN Teams t2 ON g.team2_id = t2.id
        JOIN Locations l ON g.location_id = l.id
        WHERE g.date BETWEEN ? AND ?
    """

    params = [start_date, end_date]
    
    # Add filters if the user selects specific location or team
    if location != "All":
        query += " AND l.stadium_name = ?"
        params.append(location)
    
    if team != "All":
        query += " AND (t1.name = ? OR t2.name = ?)"
        params.extend([team, team])
    
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    # Return results as a pandas DataFrame
    columns = ["Date", "Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "Location"]
    return pd.DataFrame(rows, columns=columns)
