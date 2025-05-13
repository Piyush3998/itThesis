
'''import streamlit as st
import requests
import random

st.set_page_config(page_title="Context-Aware Recommender", layout="centered")
st.title("🍽️ Context-Aware Food Recommender")

st.markdown("### Manual Recommendation Request")
user_id = st.number_input("Enter User ID", min_value=1, max_value=100)
location = st.selectbox("Current Location", ['Home', 'Work', 'Other'])
time_of_day = st.selectbox("Time of Day", ['Breakfast', 'Lunch', 'Dinner', 'Late Night'])
device = st.selectbox("Device Type", ['Mobile', 'Desktop', 'Tablet'])
weather = st.selectbox("Weather", ['Sunny', 'Rainy', 'Cloudy', 'Cold', 'Hot'])

if st.button("Get Recommendations"):
    context = {
        "location": location,
        "time_of_day": time_of_day,
        "device": device,
        "weather": weather
    }
    try:
        response = requests.post("http://127.0.0.1:5000/get_recommendations", json={"user_id": user_id, "context": context})
        if response.status_code == 200:
            st.write("### Top Recommendations:")
            st.table(response.json())
        else:
            st.error(f"Backend Error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.markdown("---")
st.markdown("### Simulate Micro-Moment Sessions")

simulate_count = st.slider("Number of Sessions", 1, 10, 3)

if st.button("Simulate Micro-Moment Sessions"):
    for i in range(simulate_count):
        sim_user_id = random.randint(1, 100)
        sim_context = {
            "location": random.choice(['Home', 'Work', 'Other']),
            "time_of_day": random.choice(['Breakfast', 'Lunch', 'Dinner', 'Late Night']),
            "device": random.choice(['Mobile', 'Desktop', 'Tablet']),
            "weather": random.choice(['Sunny', 'Rainy', 'Cloudy', 'Cold', 'Hot'])
        }
        st.subheader(f"Session {i+1}: User {sim_user_id}")
        st.write("Context:", sim_context)
        try:
            sim_response = requests.post("http://127.0.0.1:5000/get_recommendations", json={"user_id": sim_user_id, "context": sim_context})
            if sim_response.status_code == 200:
                st.table(sim_response.json())
            else:
                st.error(f"Error in session {i+1}: {sim_response.status_code}")
        except Exception as e:
            st.error(f"Simulation {i+1} failed: {e}")'''


import streamlit as st
import requests

st.set_page_config(page_title="Smart Food Recommender", layout="centered")
st.title("🍽️ Smart Food Recommender (Context-Aware)")

st.markdown("#### Get Recommendations Based on Time and Weather")

# Collect context inputs
time_of_day = st.selectbox("Time of Day", ['Breakfast', 'Lunch', 'Dinner', 'Late Night'])
weather = st.selectbox("Weather", ['Sunny', 'Rainy', 'Cloudy', 'Cold', 'Hot'])

if st.button("Get Recommendations"):
    context = {
        "time_of_day": time_of_day,
        "weather": weather
    }
    try:
        response = requests.post("http://127.0.0.1:5000/get_recommendations", json={
            "user_id": 1,  # dummy static user
            "context": context
        })
        if response.status_code == 200 and response.json():
            st.write("### Top 3 Recommendations:")
            st.table(response.json())
        else:
            st.warning("No recommendations available for the selected context.")
    except Exception as e:
        st.error(f"Request failed: {e}")