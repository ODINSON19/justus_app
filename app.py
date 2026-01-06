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

# Determine if we are on Cloud or Local to handle db connection more robustly
# (Streamlit Cloud uses st.secrets, Local uses .env)
if not os.getenv("DB_HOST"):
    # If not in env (local), try to load from st.secrets (cloud)
    # This happens automatically if we use standard st.secrets access, 
    # but our db_config.py uses os.getenv. 
    # So we can manually inject secrets into env for compatibility.
    if "DB_HOST" in st.secrets:
        os.environ["DB_HOST"] = st.secrets["DB_HOST"]
        os.environ["DB_PORT"] = st.secrets["DB_PORT"]
        os.environ["DB_NAME"] = st.secrets["DB_NAME"]
        os.environ["DB_USER"] = st.secrets["DB_USER"]
        os.environ["DB_PASSWORD"] = st.secrets["DB_PASSWORD"]

# Initialize Database on Startup
if 'db_initialized' not in st.session_state:
    if init_db():
        st.session_state['db_initialized'] = True
    else:
        st.warning("Could not connect to database. Check .env or Secrets.")

# Load CSS (Embedded directly to avoid FileNotFoundError)
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #ffd1dc, #ffffff);
}
h1, h2, h3 {
    color: #ff4d88;
    text-align: center;
}
button {
    background-color: #ff69b4 !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
}
input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

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
