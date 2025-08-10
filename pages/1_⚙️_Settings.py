import streamlit as st
import json
import os

SETTINGS_FILE = "user_prefs.json"

def load_saved_prefs():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prefs(prefs):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)

saved_prefs = load_saved_prefs()

st.title("⚙️ Settings")

# ✅ LET NEW USERS CREATE THEIR PROFILE
name = st.text_input("Enter your name")

if name:
    hide_name = st.checkbox("Hide my name in public signup list", value=False)

    if st.button("Save Preferences"):
        saved_prefs[name] = {"hide_name": hide_name}
        save_prefs(saved_prefs)
        st.success("Preferences saved!")
        st.session_state["current_user"] = name
        st.rerun()
else:
    st.info("Please enter your name to begin.")
# --- Basic Info ---

if "current_user" in st.session_state:
    name = st.session_state["current_user"]
    st.info(f"Editing preferences for: {name}")
else:
    st.warning("Please log in using the sidebar.")
    st.stop()

display_name = st.text_input("Display Name (optional)")
email = st.text_input("Email (optional)")
phone = st.text_input("Phone (optional)")

# --- Display Attendance Option ---
show_attendance = st.radio(
    "Would you like to display your name and when you'll be attending Clubhouse hours?",
    ["Yes", "No"]
)

# --- Membership Tier ---
membership = st.selectbox(
    "Select your membership tier:",
    ["1 hour per week", "2 hours per week", "3 hours per week", "4 hours per week"]
)

tier_messages = {
    "1 hour per week": "Come to socialize, help out, or do your own thing! You can select one hour per week that you would like to drop in at the Clubhouse",
    "2 hours per week": "Come to socialize, help out, or do your own thing! You can select two hours per week that you would like to drop in at the Clubhouse",
    "3 hours per week": "Come to socialize, help out, or do your own thing! You can select three hours per week that you would like to drop in at the Clubhouse",
    "4 hours per week": "Come to socialize, help out, or do your own thing! You can select four hours per week that you would like to drop in at the Clubhouse"
}

st.info(tier_messages[membership])

# --- Why Are You Joining? ---
interest_reason = st.text_area("Why are you interested in joining the Clubhouse?")

# --- Interests ---
interests = st.multiselect(
    "Interests (optional)",
    ["Art", "Music", "Fitness", "Computers", "Games", "Social Events"]
)

# --- Save ---
if st.button("Save Preferences"):
    prefs = {
        "display_name": display_name,
        "email": email,
        "phone": phone,
        "show_attendance": show_attendance,
        "membership": membership,
        "interest_reason": interest_reason,
        "interests": interests
    }
    save_user_settings(name, prefs)
    st.success("Preferences saved!")
