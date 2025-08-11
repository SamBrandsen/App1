import streamlit as st
import json
import os

st.set_page_config(page_title="Clubhouse Scheduler", layout="wide")

# Clear logout param and session state if logout detected
params = st.query_params
if "logout" in params:
    st.session_state.pop("current_user", None)
    st.session_state.pop("is_admin", None)
    # Clear the logout param so it doesn’t keep triggering
    st.query_params = {}

SETTINGS_FILE = "user_prefs.json"

def load_saved_prefs():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

saved_prefs = load_saved_prefs()
user_names = list(saved_prefs.keys())

ADMIN_PASSWORD = "letmein123"  # 🔐 Set a strong password in real use!

# Sidebar Login UI
st.sidebar.title("🔐 Login")

# Admin login section
with st.sidebar.expander("👮 Admin Login"):
    admin_attempt = st.text_input("Enter admin password", type="password", key="admin_pass")
    if admin_attempt == ADMIN_PASSWORD:
        st.session_state["is_admin"] = True
        st.session_state["current_user"] = "admin"
        st.sidebar.success("Logged in as admin")
    elif admin_attempt:
        st.sidebar.error("Incorrect password")

# Regular user login (only if not admin and no user logged in)
if "current_user" not in st.session_state or st.session_state.get("current_user") == "admin":
    if user_names:
        selected_user = st.sidebar.selectbox("Select your name", user_names)
        if st.sidebar.button("Login as user"):
            st.session_state["current_user"] = selected_user
            st.session_state["is_admin"] = False
            st.sidebar.success(f"Logged in as {selected_user}")
    else:
        st.sidebar.info("No users yet. Please set up your info in ⚙️ Settings.")
else:
    # Show currently logged in user
    st.sidebar.success(f"Logged in as {st.session_state['current_user']}")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.pop("current_user", None)
    st.session_state.pop("is_admin", None)
    st.query_params = {"logout": ["true"]}

# Optionally show user details if logged in (and not admin)
if "current_user" in st.session_state and st.session_state.get("current_user") != "admin":
    prefs = saved_prefs.get(st.session_state["current_user"], {})
    st.sidebar.markdown(f"**Membership:** {prefs.get('membership', 'N/A')}")

# Main page content
st.title("Welcome to the Clubhouse Appointments App 🎉")
st.write("Please use the sidebar to navigate to:")
st.markdown("""
- 📅 **Calendar** – to view and sign up for slots  
- ⚙️ **Settings** – to configure your info  
- 👀 **View Signups** – for moderators
""")
