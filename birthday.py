import streamlit as st
from datetime import date

def birthday_mode():
    today = date.today()

    # 🔴 CHANGE THIS TO HER BIRTHDAY
    BIRTHDAY_MONTH = 7
    BIRTHDAY_DAY = 19

    if today.month == BIRTHDAY_MONTH and today.day == BIRTHDAY_DAY:
        st.markdown("## 🎉 HAPPY BIRTHDAY MY LOVE 🎂")
        st.markdown("""
        💖 You are my favorite person  
        🌸 My safe place  
        💍 Always us, always forever  
        """)
        st.balloons()
