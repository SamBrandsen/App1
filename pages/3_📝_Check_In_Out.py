import streamlit as st
import datetime
import json
import os

CHECKINS_FILE = "checkins.json"
SIGNUPS_FILE = "signups.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

signups = load_json(SIGNUPS_FILE)
checkins = load_json(CHECKINS_FILE)

st.set_page_config(page_title="Check In / Out", layout="centered")
st.title("📝 Check In / Check Out")

if "current_user" not in st.session_state:
    st.warning("Please log in using the sidebar.")
    st.stop()

name = st.session_state["current_user"]

user_signed_slots = [slot for slot, users in signups.items() if name in users]

if not user_signed_slots:
    st.info("You have not signed up for any slots yet.")
    st.stop()

for slot_key in user_signed_slots:
    slot_dt = datetime.datetime.fromisoformat(slot_key)
    slot_str = slot_dt.strftime("%A %B %d, %I:%M %p")

    st.subheader(f"Slot: {slot_str}")

    user_checkin = checkins.get(slot_key, {}).get(name, {})
    status = user_checkin.get("status", "not_checked_in")

    if status == "not_checked_in":
        if st.button(f"Check In for {slot_str}", key=f"checkin_{slot_key}"):
            checkins.setdefault(slot_key, {})[name] = {
                "status": "checked_in",
                "checkin_time": datetime.datetime.now().isoformat()
            }
            save_json(CHECKINS_FILE, checkins)
            st.experimental_rerun()
    elif status == "checked_in":
        if st.button(f"Check Out for {slot_str}", key=f"checkout_{slot_key}"):
            checkins[slot_key][name]["status"] = "checked_out"
            checkins[slot_key][name]["checkout_time"] = datetime.datetime.now().isoformat()
            save_json(CHECKINS_FILE, checkins)
            st.experimental_rerun()
    elif status == "checked_out":
        ci_time = user_checkin.get("checkin_time", "N/A")
        co_time = user_checkin.get("checkout_time", "N/A")
        st.info(f"Checked in at: {ci_time}")
        st.info(f"Checked out at: {co_time}")

    st.divider()
