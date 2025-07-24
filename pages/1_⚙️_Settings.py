import streamlit as st

st.title("⚙️ Your Settings")

name = st.text_input("Full Name")
display_name = st.text_input("Display Name (optional)")
email = st.text_input("Email (optional)")
interests = st.multiselect(
    "Interests (optional)",
    ["Art", "Music", "Fitness", "Computers", "Games", "Social Events"]
)

if st.button("Save Preferences"):
    st.success("Preferences saved (not persisted yet).")
