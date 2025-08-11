import streamlit as st
import json
import os

st.set_page_config(page_title="Clubhouse Scheduler", layout="wide")

SETTINGS_FILE = "user_prefs.json"
ADMIN_PASSWORD = "letmein123"  # 🔐 Change in real use!

def load_saved_prefs():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prefs(prefs):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)

saved_prefs = load_saved_prefs()
user_names = list(saved_prefs.keys())

# --- SIDEBAR ACCOUNT MANAGEMENT ---
st.sidebar.title("🔐 Account")

# If logged in
if "current_user" in st.session_state:
    st.sidebar.success(f"Logged in as {st.session_state['current_user']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

# If NOT logged in
else:
    choice = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])

    if choice == "Login":
        if user_names:
            selected_user = st.sidebar.selectbox("Select your name", user_names)
            if st.sidebar.button("Log In"):
                st.session_state["current_user"] = selected_user
                st.session_state["is_admin"] = False
                st.rerun()
        else:
            st.sidebar.info("No users yet. Please sign up.")

    elif choice == "Sign Up":
        new_user = st.sidebar.text_input("Choose a username")
        if st.sidebar.button("Create Account"):
            if not new_user.strip():
                st.sidebar.error("Please enter a valid username.")
            elif new_user in saved_prefs:
                st.sidebar.error("Username already exists.")
            else:
                saved_prefs[new_user] = {"membership": "", "hide_name": False}
                save_prefs(saved_prefs)
                st.session_state["current_user"] = new_user
                st.session_state["is_admin"] = False
                st.success(f"Welcome, {new_user}! Redirecting to settings...")
                st.switch_page("pages/1_⚙️_Settings.py")

# --- ADMIN LOGIN ---
with st.sidebar.expander("👮 Admin Login"):
    admin_attempt = st.text_input("Enter admin password", type="password")
    if admin_attempt == ADMIN_PASSWORD:
        st.session_state["is_admin"] = True
        st.session_state["current_user"] = "admin"
        st.sidebar.success("Logged in as admin")
    elif admin_attempt:
        st.sidebar.error("Incorrect password")

# --- SHOW USER DETAILS IF LOGGED IN ---
if "current_user" in st.session_state and st.session_state["current_user"] != "admin":
    prefs = saved_prefs.get(st.session_state["current_user"], {})
    st.sidebar.markdown(f"**Membership:** {prefs.get('membership', 'N/A')}")

# --- MAIN PAGE CONTENT ---
st.title("Welcome to the Clubhouse Appointments App 🎉")
st.write("Please use the sidebar to navigate to:")
st.markdown("""
- 📅 **Calendar** – to view and sign up for slots  
- ⚙️ **Settings** – to configure your info  
- 👀 **View Signups** – for moderators
""")
