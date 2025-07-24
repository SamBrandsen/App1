import streamlit as st

st.set_page_config(page_title="Clubhouse Scheduler", layout="wide")

st.title("Welcome to the Clubhouse Appointments App 🎉")
st.write("Please use the sidebar to navigate to:")
st.markdown("""
- 📅 **Calendar** – to view and sign up for slots  
- ⚙️ **Settings** – to configure your info  
- 👀 **View Signups** – for moderators
""")
