import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import calendar_manager

def render_calendar_ui(user_email):
    st.header("📅 Our Shared Calendar")
    
    # --- Add New Event ---
    with st.expander("➕ Add Event"):
        with st.form("event_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Event Title", placeholder="Date Night 🍷")
                start_date = st.date_input("Date", datetime.now())
                start_time = st.time_input("Start Time", datetime.now())
            with col2:
                assigned_to = st.selectbox("Who is this for?", ["Both", "saisheashan", "ananya"])
                end_time = st.time_input("End Time", (datetime.now() + timedelta(hours=1)))
                description = st.text_area("Details", placeholder="Dinner setup, movie plan...")
            
            submitted = st.form_submit_button("Add to Calendar")
            
            if submitted and title:
                # Combine date and time
                start_dt = datetime.combine(start_date, start_time)
                end_dt = datetime.combine(start_date, end_time)
                
                # Handle end time being before start time (overnight)
                if end_dt < start_dt:
                    end_dt += timedelta(days=1)
                
                calendar_manager.create_event(
                    title, description, start_dt, end_dt, user_email, assigned_to
                )
                st.success("Event added! 🗓️")
                st.rerun()

    # --- Display Calendar ---
    events = calendar_manager.get_formatted_events_for_calendar()
    
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay,listMonth"
        },
        "initialView": "dayGridMonth",
        "navLinks": True,
        "selectable": True,
        "selectMirror": True,
    }
    
    if events:
        calendar(
            events=events,
            options=calendar_options,
            custom_css="""
                .fc-event-past { opacity: 0.8; }
                .fc-event-time { font-weight: bold; }
                .fc-event-title { font-weight: bold; }
            """
        )
    else:
        st.info("No events scheduled yet. Plan something fun! ✨")
