import sqlite3
import pandas as pd

DATABASE = 'sports_management.db'

def connect_db():
    return sqlite3.connect(DATABASE)

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
        print(f"Error: {e}")
        return False
    return True

def add_location(stadium_name, city):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Locations (stadium_name, city) VALUES (?, ?)", (stadium_name, city))
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")
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

    columns = ["Date", "Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "Location"]
    report_data = pd.DataFrame(rows, columns=columns)
    report_data["Total Points"] = report_data["Team 1 Score"] + report_data["Team 2 Score"]

    return report_data

def fetch_team_stats():
    query = """
        SELECT t.name, COUNT(g.id) as games_played
        FROM Teams t
        JOIN Games g ON t.id = g.team1_id OR t.id = g.team2_id
        GROUP BY t.id
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=["Team", "Games Played"])

def fetch_top_scoring_teams():
    query = """
        SELECT t.name, SUM(g.team1_score + g.team2_score) as total_points
        FROM Teams t
        JOIN Games g ON t.id = g.team1_id OR t.id = g.team2_id
        GROUP BY t.id
        ORDER BY total_points DESC
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=["Team", "Total Points"])

def fetch_total_wins():
    query = """
        SELECT t.name, SUM(CASE WHEN g.team1_id = t.id AND g.team1_score > g.team2_score OR g.team2_id = t.id AND g.team2_score > g.team1_score THEN 1 ELSE 0 END) as total_wins
        FROM Teams t
        JOIN Games g ON t.id = g.team1_id OR t.id = g.team2_id
        GROUP BY t.id
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=["Team", "Total Wins"])

def fetch_team_win_rate():
    query = """
        SELECT t.name, 
        SUM(CASE WHEN g.team1_id = t.id AND g.team1_score > g.team2_score OR g.team2_id = t.id AND g.team2_score > g.team1_score THEN 1 ELSE 0 END) as wins,
        COUNT(g.id) as games_played,
        ROUND((SUM(CASE WHEN g.team1_id = t.id AND g.team1_score > g.team2_score OR g.team2_id = t.id AND g.team2_score > g.team1_score THEN 1 ELSE 0 END) * 100.0) / COUNT(g.id), 2) as win_rate
        FROM Teams t
        JOIN Games g ON t.id = g.team1_id OR t.id = g.team2_id
        GROUP BY t.id
    """
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=["Team", "Wins", "Games Played", "Win Rate (%)"])
