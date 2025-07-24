import streamlit as st
import datetime

st.set_page_config(page_title="Calendar Sign-Up", layout="wide")

# Simulated database of signups
if "signups" not in st.session_state:
    st.session_state.signups = {}

if "checked_in" not in st.session_state:
    st.session_state.checked_in = {}

MAX_SIGNUPS_PER_SLOT = 3

# --------------------------
# Function to get upcoming Tuesday and Thursday
# --------------------------
def get_next_tue_thu():
    today = datetime.date.today()
    weekday = today.weekday()

    # Calculate next Tuesday
    days_until_tuesday = (1 - weekday + 7) % 7
    if days_until_tuesday == 0:
        days_until_tuesday = 7  # if today is Tuesday, get next Tuesday
    next_tuesday = today + datetime.timedelta(days=days_until_tuesday)

    # Calculate next Thursday
    days_until_thursday = (3 - weekday + 7) % 7
    if days_until_thursday == 0:
        days_until_thursday = 7  # if today is Thursday, get next Thursday
    next_thursday = today + datetime.timedelta(days=days_until_thursday)

    return [next_tuesday, next_thursday]

# --------------------------
# Generate all slots for those two days
# --------------------------
def generate_time_slots(days):
    slots = []
    for day in days:
        for hour in [9, 10, 11]:
            slot_time = datetime.datetime.combine(day, datetime.time(hour=hour))
            slots.append(slot_time)
    return slots

# --------------------------
# UI
# --------------------------
st.title("📅 Calendar Sign-Up")

name = st.text_input("Enter your name")

if not name:
    st.info("Please enter your name to view available slots.")
else:
    selected_days = get_next_tue_thu()
    all_slots = generate_time_slots(selected_days)

    for slot in all_slots:
        slot_key = slot.isoformat()
        slot_str = slot.strftime("%A %B %d, %I:%M %p")

        if slot_key not in st.session_state.signups:
            st.session_state.signups[slot_key] = []

        signups = st.session_state.signups[slot_key]
        already_signed_up = name in signups
        is_full = len(signups) >= MAX_SIGNUPS_PER_SLOT

        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{slot_str}**")
            if signups:
                st.caption(f"Signed up: {', '.join(signups)}")
            else:
                st.caption("No one signed up yet.")

        with col2:
            if already_signed_up:
                st.success("You're signed up")
            elif is_full:
                st.error("Full")
            else:
                if st.button("Sign Up", key=slot_key):
                    st.session_state.signups[slot_key].append(name)
                    st.rerun()
