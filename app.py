import streamlit as st
from db import *
import pandas as pd

# Define a function for the home screen
def home():
    st.title("Sports Team Management System")

    # Button to navigate to the "Manage Data" screen
    if st.button("Manage Data"):
        st.session_state.page = 'manage_data'

    # Button to navigate to the "Generate Reports" screen
    if st.button("Generate Reports"):
        st.session_state.page = 'generate_reports'

# Define a function for the "Manage Data" screen (Stage 2)
def manage_data():
    st.header("Manage Teams, Players, Locations, and Games")
    
    # Button to go back to home
    if st.button("Go Back"):
        st.session_state.page = 'home'

    st.subheader("Add a New Team")
    team_name = st.text_input("Team Name")
    coach_name = st.text_input("Coach Name")
    if st.button("Add Team"):
        if team_name and coach_name:
            if add_team(team_name, coach_name):
                st.success(f"Team '{team_name}' added successfully!")
            else:
                st.error("Failed to add team. Please try again.")
        else:
            st.error("Please fill in both fields.")

    st.subheader("Add a New Location")
    stadium_name = st.text_input("Stadium Name")
    city_name = st.text_input("City")
    if st.button("Add Location"):
        if stadium_name and city_name:
            if add_location(stadium_name, city_name):
                st.success(f"Location '{stadium_name}' in '{city_name}' added successfully!")
            else:
                st.error("Failed to add location. Please try again.")
        else:
            st.error("Please fill in both fields.")
    
    teams = get_teams()
    locations = get_locations()
    team_options = {team[1]: team[0] for team in teams}
    location_options = {location[1]: location[0] for location in locations}

    st.subheader("Add a New Game")
    with st.form("game_form"):
        team1 = st.selectbox("Team 1:", options=list(team_options.keys()))
        team1_score = st.number_input("Team 1 Score:", min_value=0, step=1)
        team2 = st.selectbox("Team 2:", options=list(team_options.keys()))
        team2_score = st.number_input("Team 2 Score:", min_value=0, step=1)
        location = st.selectbox("Location:", options=list(location_options.keys()))
        date = st.date_input("Date")
        submit = st.form_submit_button("Submit")
        delete = st.form_submit_button("Delete")

    if submit:
        insert_game(team_options[team1], team_options[team2], location_options[location], date, team1_score, team2_score)
        st.success(f"Game between {team1} and {team2} added successfully!")

    if delete:
        game_id = st.number_input("Game ID to delete:", min_value=0, step=1)
        if game_id:
            delete_game(game_id)
            st.success(f"Game ID {game_id} deleted successfully!")


def generate_reports():
    st.title("Generate Reports")
    
    # Fetch location options from the database
    location_options = fetch_locations()
    team_options = fetch_teams()

    # Let the user filter by date range, location, or teams
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    location = st.selectbox("Location:", options=["All"] + location_options)
    team = st.selectbox("Team:", options=["All"] + team_options)

    if st.button("Generate Report"):
        # Query database using filters
        report_data = fetch_report_data(start_date, end_date, location, team)

        if report_data.empty:
            st.warning("No games found for the selected criteria.")
        else:
            # Display results as a table
            st.dataframe(report_data)



def fetch_locations():
    query = "SELECT stadium_name FROM Locations"
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    
    # Return a list of location names
    return [row[0] for row in rows]


def fetch_teams():
    query = "SELECT name FROM Teams"
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    
    # Return a list of team names
    return [row[0] for row in rows]

# Initialize session state if not already initialized
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation logic based on session state
if st.session_state.page == 'home':
    home()
elif st.session_state.page == 'manage_data':
    manage_data()
elif st.session_state.page == 'generate_reports':
    generate_reports()
