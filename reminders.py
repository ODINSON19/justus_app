import streamlit as st
from datetime import datetime
from email_service import send_email

HER_EMAIL = "ananyamukundan900@gmail.com"

def kiss_reminder():
    st.subheader("💋 Kiss Reminder")

    kiss_time = st.time_input("Choose kiss time 💖")
    message = st.text_input(
        "Message",
        "Mandatory kiss time 💋❤️"
    )

    if st.button("Set Kiss Reminder & Email Her 💞"):
        subject = "💋 Kiss Reminder Alert!"
        body = f"It's time for a kiss! 😘\n\nTarget Time: {kiss_time}\nMessage: {message}\n\nSent from Just Us App 💖"
        
        if send_email(HER_EMAIL, subject, body):
            st.success(f"📧 Email sent to her! ⏰ {kiss_time} — {message}")
            st.balloons()


def hug_reminder():
    st.subheader("🤗 Hug Reminder")

    hug_msg = st.text_input(
        "Hug message",
        "Sending you the warmest hug 🤗❤️"
    )

    if st.button("Send Hug Email 🤍"):
        subject = "🤗 A Big Hug for You!"
        body = f"You received a virtual hug! 🫂\n\nMessage: {hug_msg}\n\nSent from Just Us App 💖"
        
        if send_email(HER_EMAIL, subject, body):
            st.success("📧 Hug email sent! " + hug_msg)
            st.balloons()
