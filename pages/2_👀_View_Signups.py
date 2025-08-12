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

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

saved_prefs = load_json(SETTINGS_FILE)
signups = load_json(SIGNUPS_FILE)
checkins = load_json(CHECKINS_FILE)

is_admin = st.session_state.get("is_admin", False)
st.set_page_config(page_title="Calendar Sign-Up", layout="wide")

MAX_SIGNUPS_PER_SLOT = 3

def get_next_tue_thu():
    today = datetime.date.today()
    weekday = today.weekday()
    days_until_tuesday = (1 - weekday + 7) % 7 or 7
    days_until_thursday = (3 - weekday + 7) % 7 or 7
    return [today + datetime.timedelta(days=days_until_tuesday),
            today + datetime.timedelta(days=days_until_thursday)]

def generate_time_slots(days):
    slots = []
    for day in days:
        for hour in [9, 10, 11]:
            slot_time = datetime.datetime.combine(day, datetime.time(hour=hour))
            slots.append(slot_time)
    return slots

if "current_user" not in st.session_state:
    st.warning("Please log in using the sidebar.")
    st.stop()

name = st.session_state["current_user"]

selected_days = get_next_tue_thu()
all_slots = generate_time_slots(selected_days)

st.title("📅 Calendar Sign-Up & Check-In")

for slot in all_slots:
    slot_key = slot.isoformat()
    slot_str = slot.strftime("%A %B %d, %I:%M %p")

    if slot_key not in signups:
        signups[slot_key] = []
    if slot_key not in checkins:
        checkins[slot_key] = {}

    signups_for_slot = signups[slot_key]
    checkins_for_slot = checkins[slot_key]

    col1, col2, col3 = st.columns([4, 2, 3])
    with col1:
        st.write(f"**{slot_str}**")
        if signups_for_slot:
            # Show names or hidden based on prefs
            visible_signups = []
            for user in signups_for_slot:
                prefs = saved_prefs.get(user, {})
                show_attendance = prefs.get("show_attendance", True)
                if is_admin or show_attendance:
                    visible_signups.append(user)
                else:
                    visible_signups.append("🔒 Hidden")
            st.caption(f"Signed up: {', '.join(visible_signups)}")
        else:
            st.caption("No one signed up yet.")

    with col2:
        if name in signups_for_slot:
            status = checkins_for_slot.get(name, {}).get("status", "not_checked_in")
            if status == "not_checked_in":
                if st.button("Check In", key=f"checkin_{slot_key}"):
                    checkins_for_slot[name] = {
                        "status": "checked_in",
                        "checkin_time": datetime.datetime.now().isoformat()
                    }
                    save_json(CHECKINS_FILE, checkins)
                    st.experimental_rerun()
            elif status == "checked_in":
                if st.button("Check Out", key=f"checkout_{slot_key}"):
                    checkins_for_slot[name]["status"] = "checked_out"
                    checkins_for_slot[name]["checkout_time"] = datetime.datetime.now().isoformat()
                    save_json(CHECKINS_FILE, checkins)
                    st.experimental_rerun()
            elif status == "checked_out":
                st.info("Checked out")
        else:
            if len(signups_for_slot) >= MAX_SIGNUPS_PER_SLOT:
                st.error("Full")
            else:
                if st.button("Sign Up", key=f"signup_{slot_key}"):
                    signups_for_slot.append(name)
                    save_json(SIGNUPS_FILE, signups)
                    st.experimental_rerun()

    with col3:
        # Show check-in/out summary for current user
        if is_admin:
            st.caption("Check-in/out status:")
            for user in signups_for_slot:
                info = checkins_for_slot.get(user, {"status": "not_checked_in"})
                ci_time = info.get("checkin_time", "N/A")
                co_time = info.get("checkout_time", "N/A")
                status = info.get("status", "not_checked_in")
                st.write(f"- {user}: {status}, In: {ci_time}, Out: {co_time}")
        else:
            if name in checkins_for_slot:
                info = checkins_for_slot[name]
                ci_time = info.get("checkin_time", "N/A")
                co_time = info.get("checkout_time", "N/A")
                st.write(f"Check-in: {ci_time}")
                st.write(f"Check-out: {co_time}")
