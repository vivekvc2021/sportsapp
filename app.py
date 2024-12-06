import streamlit as st
from db import *

teams = get_teams()
locations = get_locations()

team_options = {team[1]: team[0] for team in teams}
location_options = {location[1]: location[0] for location in locations}

st.header("Add a New Team")

team_name = st.text_input("Team Name")
coach_name = st.text_input("Coach Name")

if st.button("Add Team"):
    if team_name and coach_name:  # Ensure inputs are filled
        if add_team(team_name, coach_name):
            st.success(f"Team '{team_name}' added successfully!")
        else:
            st.error("Failed to add team. Please try again.")
    else:
        st.error("Please fill in both fields.")

st.header("Add a New Location")

stadium_name = st.text_input("Stadium Name")
city_name = st.text_input("City")

if st.button("Add Location"):
    if stadium_name and city_name:  # Ensure inputs are filled
        if add_location(stadium_name, city_name):
            st.success(f"Location '{stadium_name}' in '{city_name}' added successfully!")
        else:
            st.error("Failed to add location. Please try again.")
    else:
        st.error("Please fill in both fields.")

st.title("Game Interface (Screen Two)")

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
