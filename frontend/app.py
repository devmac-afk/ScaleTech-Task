
import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(layout="wide", page_title="Sleeper Bus Booking")

# Constants
API_URL = "http://127.0.0.1:8000"

st.title("🚌 Sleeper Bus Ticket Booking System")
st.subheader("Route: Ahmedabad → Mumbai")

# --- Sidebar: Station Info ---
st.sidebar.header("📍 Route Stations")
try:
    response = requests.get(f"{API_URL}/stations")
    if response.status_code == 200:
        stations = response.json()
        for station in stations:
            st.sidebar.text(f"{station['arrival_time']} - {station['name']}")
    else:
        st.sidebar.error("Could not load stations.")
except Exception:
    st.sidebar.warning("Backend mock running? Start backend first.")

# --- Prediction Model (Mock) ---
st.sidebar.markdown("---")
st.sidebar.header("🔮 Booking Probability")
days_prior = st.sidebar.slider("Days before travel", 0, 30, 5)
seat_type_pref = st.sidebar.selectbox("Preferred Seat Type", ["Sleeper", "Seater"])
is_weekend = st.sidebar.checkbox("Is it a Weekend?")

if st.sidebar.button("Predict Confirmation Chance"):
    try:
        resp = requests.post(f"{API_URL}/predict-probability", json={
            "days_prior": days_prior,
            "seat_type": seat_type_pref,
            "is_weekend": is_weekend
        })
        if resp.status_code == 200:
            data = resp.json()
            st.sidebar.metric(label="Probability", value=f"{data['confirmation_probability']}%")
            st.sidebar.info(data['analysis'])
    except Exception as e:
        st.sidebar.error(f"Error connecting to ML API: {e}")

# --- Main Area: Seat Map ---

st.header("💺 Select a Seat")

def get_seat_color(is_booked):
    return "🔴" if is_booked else "🟢"

try:
    response = requests.get(f"{API_URL}/seats")
    if response.status_code == 200:
        seats = response.json()
        
        # Separate Upper and Lower
        lower_seats = [s for s in seats if s['type'] == 'Lower Sleeper']
        upper_seats = [s for s in seats if s['type'] == 'Upper Sleeper']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Lower Berths (L)")
            # Create a grid
            for i in range(0, len(lower_seats), 2):
                c1, c2 = st.columns(2)
                if i < len(lower_seats):
                    s = lower_seats[i]
                    with c1:
                        st.button(f"{s['seat_id']} {get_seat_color(s['is_booked'])}", key=s['seat_id'], help=f"Price: {s['price']}")
                if i+1 < len(lower_seats):
                    s = lower_seats[i+1]
                    with c2:
                        st.button(f"{s['seat_id']} {get_seat_color(s['is_booked'])}", key=s['seat_id'], help=f"Price: {s['price']}")

        with col2:
            st.subheader("Upper Berths (U)")
            for i in range(0, len(upper_seats), 2):
                c1, c2 = st.columns(2)
                if i < len(upper_seats):
                    s = upper_seats[i]
                    with c1:
                        st.button(f"{s['seat_id']} {get_seat_color(s['is_booked'])}", key=s['seat_id'], help=f"Price: {s['price']}")
                if i+1 < len(upper_seats):
                    s = upper_seats[i+1]
                    with c2:
                        st.button(f"{s['seat_id']} {get_seat_color(s['is_booked'])}", key=s['seat_id'], help=f"Price: {s['price']}")
                        
        # --- Booking Section ---
        st.divider()
        st.header("📝 Booking Details")
        
        # Determine accessible seats for dropdown
        available_seats = [s['seat_id'] for s in seats if not s['is_booked']]
        booked_seats_by_me = [s['seat_id'] for s in seats if s['is_booked']] # Simplified for prototype
        
        action = st.radio("Choose Action", ["Book a Seat", "Cancel Booking"])
        
        if action == "Book a Seat":
            if not available_seats:
                st.warning("No seats available!")
            else:
                with st.form("booking_form"):
                    selected_seat = st.selectbox("Select Seat", available_seats)
                    user_name = st.text_input("Passenger Name")
                    meal_pref = st.selectbox("Meal Preference", ["None", "Veg", "Non-Veg"])
                    submitted = st.form_submit_button("Confirm Booking")
                    
                    if submitted:
                        if not user_name:
                            st.error("Please enter a name.")
                        else:
                            # Call API
                            req_data = {"seat_id": selected_seat, "user_name": user_name, "meal": meal_pref}
                            res = requests.post(f"{API_URL}/book-seat", json=req_data)
                            if res.status_code == 200:
                                st.success(f"Success! Seat {selected_seat} booked for {user_name}.")
                                st.rerun()
                            else:
                                st.error(res.json()['detail'])

        elif action == "Cancel Booking":
            if not booked_seats_by_me:
                st.info("No bookings to cancel.")
            else:
                 with st.form("cancel_form"):
                    cancel_seat = st.selectbox("Select Seat to Cancel", booked_seats_by_me)
                    user_name_confirm = st.text_input("Confirm Passenger Name") # Mock check
                    cancel_submit = st.form_submit_button("Cancel Booking")
                    
                    if cancel_submit:
                         # Call API
                        req_data = {"seat_id": cancel_seat, "user_name": user_name_confirm}
                        res = requests.post(f"{API_URL}/cancel-booking", json=req_data)
                        if res.status_code == 200:
                            st.success(f"Booking for Seat {cancel_seat} cancelled.")
                            st.rerun()
                        else:
                            st.error(res.json()['detail'])

    else:
        st.error("Failed to fetch seat data. Is backend running?")

except requests.exceptions.ConnectionError:
    st.error("⚠️ Backend Connection Error. Please run: `uvicorn backend.main:app --reload`")

