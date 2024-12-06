import sqlite3

DATABASE = 'sports_management.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
        conn.commit()

def get_teams():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Teams")
        return cursor.fetchall()

def get_locations():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, stadium_name FROM Locations")
        return cursor.fetchall()

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

def insert_game(team1_id, team2_id, location_id, date, team1_score, team2_score):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Games (team1_id, team2_id, location_id, date, team1_score, team2_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (team1_id, team2_id, location_id, date, team1_score, team2_score))
        conn.commit()

def delete_game(game_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Games WHERE id = ?", (game_id,))
        conn.commit()
