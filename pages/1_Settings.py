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

# --- New user signup ---
if "current_user" not in st.session_state:
    st.info("New user? Create your profile below:")
    with st.form("new_user_form"):
        new_user = st.text_input("Enter your desired username")
        submit = st.form_submit_button("Create Profile")
        if submit:
            if not new_user.strip():
                st.error("Please enter a valid username.")
            elif new_user in saved_prefs:
                st.error("That username already exists. Please pick another.")
            else:
                saved_prefs[new_user] = {
                    "show_attendance": True,  # default to showing attendance
                    "membership": "1 hour per week"
                }
                save_prefs(saved_prefs)
                st.success(f"Profile created for '{new_user}'. Please log in using the sidebar.")
    st.stop()

# --- Editing settings ---
st.title("Settings")

name = st.session_state["current_user"]
prefs = saved_prefs.get(name, {})

# --- Display Attendance ---
current_attendance = prefs.get("show_attendance", True)
show_attendance = st.radio(
    "Display my name and attendance in the public signup list?",
    ["Yes", "No"],
    index=0 if current_attendance else 1
)

# --- Membership Tier ---
membership_options = [
    "1 hour per week",
    "2 hours per week",
    "3 hours per week",
    "4 hours per week"
]
current_membership = prefs.get("membership", membership_options[0])
if current_membership not in membership_options:
    current_membership = membership_options[0]

membership = st.selectbox(
    "Select your membership tier:",
    membership_options,
    index=membership_options.index(current_membership)
)

tier_messages = {
    "1 hour per week": "Come to socialize, help out, or do your own thing! You can select one hour per week that you would like to drop in at the Clubhouse",
    "2 hours per week": "Come to socialize, help out, or do your own thing! You can select two hours per week that you would like to drop in at the Clubhouse",
    "3 hours per week": "Come to socialize, help out, or do your own thing! You can select three hours per week that you would like to drop in at the Clubhouse",
    "4 hours per week": "Come to socialize, help out, or do your own thing! You can select four hours per week that you would like to drop in at the Clubhouse"
}
st.info(tier_messages[membership])

# --- Why Are You Joining? ---
interest_reason = st.text_area("Why are you interested in joining the Clubhouse?", value=prefs.get("interest_reason", ""))

# --- Interests ---
interests = st.multiselect(
    "Interests (optional)",
    ["Art", "Music", "Fitness", "Computers", "Games", "Social Events"],
    default=prefs.get("interests", [])
)

# --- Save Button ---
if st.button("Save Preferences"):
    saved_prefs[name] = {
        "show_attendance": (show_attendance == "Yes"),
        "membership": membership,
        "interest_reason": interest_reason,
        "interests": interests
    }
    save_prefs(saved_prefs)
    st.success("Preferences saved!")
    st.rerun()
