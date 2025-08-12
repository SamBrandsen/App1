import streamlit as st
import datetime
import json
import os

# --- Load your JSON files ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

SIGNUPS_FILE = "signups.json"
CHECKINS_FILE = "checkins.json"

signups = load_json(SIGNUPS_FILE)
checkins = load_json(CHECKINS_FILE)

# --- Check admin flag early ---
is_admin = st.session_state.get("is_admin", False)

if not is_admin:
    st.error("You must be an admin to view this page.")
    st.stop()  # STOP execution here so nothing else renders

# --- If we reach here, we know user is admin ---
st.title("👀 Admin View: All Signups and Check-ins")

for slot_key, users_signed_up in signups.items():
    slot_dt = datetime.datetime.fromisoformat(slot_key)
    slot_str = slot_dt.strftime("%A %B %d, %I:%M %p")
    st.subheader(f"Slot: {slot_str}")

    if not users_signed_up:
        st.write("No signups.")
        continue

    checkins_for_slot = checkins.get(slot_key, {})

    for user in users_signed_up:
        info = checkins_for_slot.get(user, {"status": "not_checked_in"})
        status = info.get("status", "not_checked_in")
        ci_time = info.get("checkin_time", "N/A")
        co_time = info.get("checkout_time", "N/A")

        st.write(f"- {user} — Status: {status}, Check-in: {ci_time}, Check-out: {co_time}")

