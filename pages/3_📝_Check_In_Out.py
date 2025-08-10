import streamlit as st

st.set_page_config(page_title="Check In / Out", layout="centered")
st.title("📝 Check In / Check Out")

st.subheader("Check In")
with st.form("checkin"):
    st.write("How are you feeling before spending time at the Clubhouse?")
    mood_in = st.slider("Mood", 1, 5, 3, help="1 = 😢  5 = 😄")
    checkin_submitted = st.form_submit_button("Check In")

if checkin_submitted:
    st.success("Check-In submitted!")

st.divider()

st.subheader("Check Out")
with st.form("checkout"):
    st.write("How are you feeling after spending time at the Clubhouse?")
    mood_out = st.slider("Mood", 1, 5, 3)

    st.write("What did you spend your time doing today?")
    activities = st.multiselect(
        "Select all that apply",
        [
            "Vocational (cleaning, hospitality, groundskeeping)",
            "Chill (games, art, reading)",
            "Movement (outdoor games, indoor games, yoga)"
        ]
    )

    hobbies = st.text_input("What hobbies did you enjoy today?")
    checkout_submitted = st.form_submit_button("Check Out")

if checkout_submitted:
    st.success("Check-Out submitted! Thank you for participating.")
