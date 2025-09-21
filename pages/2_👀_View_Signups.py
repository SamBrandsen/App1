import streamlit as st
import datetime
import json
import os

# --- File paths ---
SETTINGS_FILE = "user_prefs.json"
SIGNUPS_FILE = "signups.json"
CHECKINS_FILE = "checkins.json"

# --- Helper functions ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# --- Load data ---
saved_prefs = load_json(SETTINGS_FILE)
signups = load_json(SIGNUPS_FILE)
checkins = load_json(CHECKINS_FILE)

# --- Ensure user is logged in ---
if "current_user" not in st.session_state:
    st.warning("Please log in using the sidebar.")
    st.stop()

user_name = st.session_state["current_user"]
is_admin = st.session_state.get("is_admin", False)

# --- Session rerun trigger ---
if "rerun" not in st.session_state:
    st.session_state.rerun = False

# --- Generate next future sessions (Wed/Friday) ---
def get_next_sessions(n_sessions=4):
    today = datetime.datetime.now()
    sessions = []

    # weekday number -> (start_hour, start_minute, duration_hours)
    session_rules = {
        2: (14, 0, 2),    # Wednesday 2:00–4:00
        4: (14, 30, 2)    # Friday 2:30–4:30
    }

    check_date = today.date()
    while len(sessions) < n_sessions:
        weekday = check_date.weekday()
        if weekday in session_rules:
            start_hour, start_minute, duration_hours = session_rules[weekday]
            start_dt = datetime.datetime.combine(check_date, datetime.time(start_hour, start_minute))
            if start_dt > today:
                end_dt = start_dt + datetime.timedelta(hours=duration_hours)
                sessions.append({
                    "start": start_dt,
                    "end": end_dt,
                    "max_capacity": 12,
                    "day": start_dt.strftime("%A")
                })
        check_date += datetime.timedelta(days=1)

    return sessions

sessions = get_next_sessions(n_sessions=4)

# --- Ensure all sessions exist in signups and checkins ---
for sess in sessions:
    slot_key = sess["start"].isoformat()
    if slot_key not in signups:
        signups[slot_key] = []
    if slot_key not in checkins:
        checkins[slot_key] = {}

# --- Page title ---
st.title("📅 Clubhouse Sessions Sign-Up & Check-In")

# --- Display sessions ---
for sess in sessions:
    slot_key = sess["start"].isoformat()
    start_str = sess["start"].strftime("%A %B %d, %I:%M %p")
    end_str = sess["end"].strftime("%I:%M %p")
    st.subheader(f"{sess['day']} Session: {start_str} - {end_str}")
    st.caption(f"Maximum Participants: {sess['max_capacity']}")

    session_signups = signups[slot_key]
    session_checkins = checkins[slot_key]

    col1, col2, col3 = st.columns([4, 2, 3])

    # --- Column 1: Participant Names ---
    with col1:
        if session_signups:
            visible_names = []
            for uname in session_signups:
                prefs = saved_prefs.get(uname, {})
                show_attendance = prefs.get("show_attendance", True)
                visible_names.append(uname if (is_admin or show_attendance) else "🔒 Hidden")
            st.caption(f"Signed up: {', '.join(visible_names)}")
        else:
            st.caption("No one signed up yet.")

    # --- Column 2: User actions ---
    signup_clicked = False
    checkin_clicked = False
    checkout_clicked = False

    with col2:
        if user_name in session_signups:
            status = session_checkins.get(user_name, {}).get("status", "not_checked_in")
            if status == "not_checked_in":
                checkin_clicked = st.button("Check In", key=f"checkin_{slot_key}")
            elif status == "checked_in":
                checkout_clicked = st.button("Check Out", key=f"checkout_{slot_key}")
            elif status == "checked_out":
                st.info("Checked out")
        else:
            if len(session_signups) >= sess["max_capacity"]:
                st.error("Full")
            else:
                signup_clicked = st.button("Sign Up", key=f"signup_{slot_key}")

    # --- Column 3: Admin / user info ---
    with col3:
        if is_admin:
            st.caption("Check-in/out status:")
            for uname in session_signups:
                info = session_checkins.get(uname, {"status": "not_checked_in"})
                ci_time = info.get("checkin_time", "N/A")
                co_time = info.get("checkout_time", "N/A")
                st.write(f"- {uname}: {info.get('status', 'not_checked_in')}, In: {ci_time}, Out: {co_time}")
        else:
            if user_name in session_checkins:
                info = session_checkins[user_name]
                ci_time = info.get("checkin_time", "N/A")
                co_time = info.get("checkout_time", "N/A")
                st.write(f"Check-in: {ci_time}")
                st.write(f"Check-out: {co_time}")

    # --- Process button clicks ---
    if signup_clicked:
        session_signups.append(user_name)
        save_json(SIGNUPS_FILE, signups)
        st.session_state.rerun = not st.session_state.rerun

    if checkin_clicked:
        session_checkins[user_name] = {
            "status": "checked_in",
            "checkin_time": datetime.datetime.now().isoformat()
        }
        save_json(CHECKINS_FILE, checkins)
        st.session_state.rerun = not st.session_state.rerun

    if checkout_clicked:
        session_checkins[user_name]["status"] = "checked_out"
        session_checkins[user_name]["checkout_time"] = datetime.datetime.now().isoformat()
        save_json(CHECKINS_FILE, checkins)
        st.session_state.rerun = not st.session_state.rerun

