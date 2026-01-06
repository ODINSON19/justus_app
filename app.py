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

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    return f"data:image/{img_format};base64,{bin_str}"

# Try to use local image if it exists, otherwise fallback to URL
bg_image_css = ""
if os.path.exists("image1.jpeg"):
    bg_img_url = get_img_with_href("image1.jpeg")
    bg_image_css = f'background-image: url("{bg_img_url}");'
else:
    # Fallback
    bg_image_css = 'background-image: url("https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=2070&auto=format&fit=crop");'

# Load CSS (Embedded directly to avoid FileNotFoundError)
# Added Background Image styling
st.markdown(f"""
<style>
/* Background Image for the whole app */
.stApp {{
    {bg_image_css}
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Semi-transparent white container for content readability */
.block-container {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 20px;
    margin-top: 2rem;
}}

body {{
    background: transparent; /* Let stApp background show through */
}}
h1, h2, h3 {{
    color: #ff4d88;
    text-align: center;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}}
button {{
    background-color: #ff69b4 !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 10px 20px !important;
    border: none !important;
    font-weight: bold !important;
}}
input, textarea {{
    border-radius: 10px !important;
    border: 2px solid #ffb7b2 !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 10px;
    padding: 10px 20px;
}}
.stTabs [aria-selected="true"] {{
    background-color: #ff69b4 !important;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- APP ----------------

# Login Section
if 'user_email' not in st.session_state:
    st.title("💖 Just Us Login")
    email_input = st.text_input("Enter your email 💌")
    if st.button("Enter ❤️"):
        if check_access(email_input):
            st.session_state['user_email'] = email_input.lower().strip()
            st.rerun()
        else:
            st.error("🚫 This app is only for us 💔")
else:
    # User is logged in
    email = st.session_state['user_email']
    
    # 🎂 BIRTHDAY PAGE FOR HER 🎂
    # Only show this if it's HER email
    if email == "ananyamukundan900@gmail.com" and 'birthday_seen' not in st.session_state:
        st.markdown("<h1 style='font-size: 60px;'>🎂 Happy Birthday My Love! ❤️</h1>", unsafe_allow_html=True)
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdtY2J6ZnB5eGl5aDdtY2J6ZnB5eGl5aDdtY2J6ZnB5eGl5aDdtY2J6ZnB5eGl5aCZlcD12MV9naWZzX3NlYXJjaCZN/l4pTfx2qLSznwEdTu/giphy.gif", use_column_width=True)
        
        st.markdown("""
        ### My Everything 💖
        
        Happy birthday my everything! You are my life, my soul, and you make me feel alive and happy. 
        I love the way you are and I love the way you look at me. 
        When I am with you, it feels like it is **Us vs The World**.
        
        So I call this... **Just Us**. ❤️
        """)
        
        if st.button("Enter Our World 🌍✨"):
            st.session_state['birthday_seen'] = True
            st.balloons()
            st.rerun()
            
    else:
        # MAIN DASHBOARD (For You OR Her after she clicks enter)
        st.title("💖 Just Us")
        st.caption(f"Logged in as: {email}")

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
            
        if st.button("Logout 🔒"):
            del st.session_state['user_email']
            if 'birthday_seen' in st.session_state:
                del st.session_state['birthday_seen']
            st.rerun()
