from db_config import execute_query

def create_event(title, description, start_time, end_time, created_by, assigned_to):
    """Create a new calendar event."""
    query = """
    INSERT INTO calendar_events (title, description, start_time, end_time, created_by, assigned_to)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    # Simply using execute_query helper wouldn't return the ID easily with current helper design 
    # for single value without modifying it, but let's stick to the pattern or improve it.
    # The helper 'execute_query' with fetch=True returns a list of dictionaries.
    
    result = execute_query(query, (title, description, start_time, end_time, created_by, assigned_to), fetch=True)
    if result:
        return result[0]['id']
    return None

def get_events(start_date=None, end_date=None):
    """Retrieve all events, optionally filtering by date range."""
    # For simplicity, we'll fetch all events for now, or filter if params provided
    if start_date and end_date:
        query = """
        SELECT * FROM calendar_events 
        WHERE start_time >= %s AND end_time <= %s
        ORDER BY start_time ASC;
        """
        return execute_query(query, (start_date, end_date), fetch=True)
    else:
        query = "SELECT * FROM calendar_events ORDER BY start_time ASC;"
        return execute_query(query, fetch=True)

def delete_event(event_id):
    """Delete an event by ID."""
    query = "DELETE FROM calendar_events WHERE id = %s;"
    return execute_query(query, (event_id,))

def get_formatted_events_for_calendar():
    """Get events in the format required by streamlit-calendar."""
    raw_events = get_events()
    formatted_events = []
    
    if not raw_events:
        return []
        
    for event in raw_events:
        # Determine color based on who it's assigned to or created by
        color = "#FF6C6C" # Default red
        if event['assigned_to'] == 'Both':
            color = "#9B59B6" # Purple
        elif 'saisheashan' in  event.get('assigned_to', '').lower():
            color = "#3498DB" # Blue
        elif 'ananya' in event.get('assigned_to', '').lower(): 
            color = "#E91E63" # Pink
            
        formatted_events.append({
            "id": event['id'],
            "title": event['title'],
            "start": event['start_time'].isoformat(),
            "end": event['end_time'].isoformat(),
            "backgroundColor": color,
            "borderColor": color,
            "extendedProps": {
                "description": event['description'],
                "assigned_to": event['assigned_to']
            }
        })
        
    return formatted_events
