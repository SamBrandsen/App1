import streamlit as st
import json
import os

st.set_page_config(page_title="Clubhouse Scheduler", layout="wide")


SETTINGS_FILE = "user_prefs.json"

def load_saved_prefs():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

saved_prefs = load_saved_prefs()
user_names = list(saved_prefs.keys())

ADMIN_PASSWORD = "letmein123"  # 🔐 Set a strong password in real use!

# Existing: Sidebar title
st.sidebar.title("🔐 Login")


if user_names:
    selected_user = st.sidebar.selectbox("Select your name", user_names)
    st.session_state["current_user"] = selected_user
    st.session_state["is_admin"] = False  # regular user
    st.sidebar.success(f"Logged in as {selected_user}")
else:
    st.sidebar.info("No users yet. Please set up your info in ️Settings.")



# Admin login
with st.sidebar.expander("👮 Admin Login"):
    admin_attempt = st.text_input("Enter admin password", type="password")
    if admin_attempt == ADMIN_PASSWORD:
        st.session_state["is_admin"] = True
        st.session_state["current_user"] = "admin"
        st.sidebar.success("Logged in as admin")
    elif admin_attempt:
        st.sidebar.error("Incorrect password")

#if user_names:
#    selected_user = st.sidebar.selectbox("Select your name", user_names)
#    st.session_state["current_user"] = selected_user
#    st.sidebar.success(f"Logged in as {selected_user}")
#else:
#    st.sidebar.info("No users yet. Please set up your info in ⚙️ Settings.")

# Optionally show user details
if "current_user" in st.session_state:
    prefs = saved_prefs.get(st.session_state["current_user"], {})
    st.sidebar.markdown(f"**Membership:** {prefs.get('membership', 'N/A')}")



st.title("Welcome to the Clubhouse Appointments App 🎉")
st.write("Please use the sidebar to navigate to:")
st.markdown("""
- 📅 **Calendar** – to view and sign up for slots  
- ⚙️ **Settings** – to configure your info  
- 👀 **View Signups** – for moderators
""")
