import streamlit as st
import os
from dotenv import load_dotenv

# Load env before imports that might use it
load_dotenv()

from auth import check_access
from reminders import kiss_reminder, hug_reminder
from birthday import birthday_mode
from db_init import init_db
import calendar_ui
import album_ui

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="💖 Just Us",
    layout="centered"
)

# Initialize Database on Startup
if 'db_initialized' not in st.session_state:
    if init_db():
        st.session_state['db_initialized'] = True
    else:
        st.error("Connection to Database Failed. Please check .env settings.")

# Load CSS
with open("assets/hearts.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- APP ----------------
st.title("💖 Just Us")

email = st.text_input("Enter your email 💌")

if email:
    if check_access(email):

        birthday_mode()

        # Tabs Layout
        tab1, tab2, tab3, tab4 = st.tabs(
            ["💋 Kiss", "🤗 Hug", "📅 Calendar", "📚 Albums"]
        )

        with tab1:
            kiss_reminder()

        with tab2:
            hug_reminder()

        with tab3:
            calendar_ui.render_calendar_ui(email)
            
        with tab4:
            album_ui.render_album_ui(email)

    else:
        st.error("🚫 This app is only for us 💔")
