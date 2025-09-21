import streamlit as st
import json
import os

SETTINGS_FILE = "user_prefs.json"

# --- Load / save helper functions ---
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
                    "show_attendance": True  # default
                }
                save_prefs(saved_prefs)
                st.success(f"Profile created for '{new_user}'. Please log in using the sidebar.")
    st.stop()

# --- Settings page ---
st.title("Settings")

name = st.session_state["current_user"]
prefs = saved_prefs.get(name, {})

# --- Show Attendance ---
current_attendance = prefs.get("show_attendance", True)
show_attendance = st.radio(
    "Display my name in the public signup list?",
    ["Yes", "No"],
    index=0 if current_attendance else 1
)

# --- Save Button ---
if st.button("Save Preferences"):
    saved_prefs[name] = {
        "show_attendance": (show_attendance == "Yes")
    }
    save_prefs(saved_prefs)
    st.success("Preferences saved!")
    st.session_state.rerun = not st.session_state.rerun  # trigger page refresh

