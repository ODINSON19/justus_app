import streamlit as st
from datetime import datetime

def kiss_reminder():
    st.subheader("💋 Kiss Reminder")

    kiss_time = st.time_input("Choose kiss time 💖")
    message = st.text_input(
        "Message",
        "Mandatory kiss time 💋❤️"
    )

    if st.button("Set Kiss Reminder 💞"):
        st.success(f"⏰ {kiss_time} — {message}")
        st.balloons()


def hug_reminder():
    st.subheader("🤗 Hug Reminder")

    hug_msg = st.text_input(
        "Hug message",
        "Sending you the warmest hug 🤗❤️"
    )

    if st.button("Send Hug 🤍"):
        st.success(hug_msg)
        st.balloons()
