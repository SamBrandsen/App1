import streamlit as st
import datetime
import json
import os

SETTINGS_FILE = "user_prefs.json"
SIGNUPS_FILE = "signups.json"
CHECKINS_FILE = "checkins.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

saved_prefs = load_json(SETTINGS_FILE)
signups = load_json(SIGNUPS_FILE)
checkins = load_json(CHECKINS_FILE)

st.set_page_config(page_title="Admin View: Signups & Check-ins", layout="wide")


st.title("👀 Admin View: All Signups and Check-ins")

for slot_key, users_signed_up in signups.items():
    slot_dt = datetime.datetime.fromisoformat(slot_key)
    slot_str = slot_dt.strftime("%A %B %d, %I:%M %p")
    st.subheader(f"Slot: {slot_str}")

    if not users_signed_up:
        st.write("No signups.")
        continue

    # Get checkins for this slot (might be empty)
    checkins_for_slot = checkins.get(slot_key, {})

    for user in users_signed_up:
        status_info = checkins_for_slot.get(user, {"status": "not_checked_in"})
        status = status_info.get("status", "not_checked_in")
        ci_time = status_info.get("checkin_time", "N/A")
        co_time = status_info.get("checkout_time", "N/A")

        st.write(f"- **{user}** — Status: {status}, Check-in: {ci_time}, Check-out: {co_time}")



# Simple admin auth: make sure user is admin
if not st.session_state.get("is_admin", False):
    st.warning("You must be an admin to view this page.")
    st.stop()

all_slots = sorted(signups.keys())
if not all_slots:
    st.info("No signup data found.")
    st.stop()

for slot_key in all_slots:
    slot_dt = datetime.datetime.fromisoformat(slot_key)
    slot_str = slot_dt.strftime("%A %B %d, %I:%M %p")

