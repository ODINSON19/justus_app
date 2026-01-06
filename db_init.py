import os
from db_config import get_db_connection

def init_db():
    """Initialize the database with the schema."""
    conn = get_db_connection()
    if not conn:
        print("Could not connect to database. Please check your credentials in .env")
        return False
    
    try:
        with open('db_schema.sql', 'r') as f:
            schema = f.read()
            
        cur = conn.cursor()
        cur.execute(schema)
        conn.commit()
        print("Database initialized successfully!")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    init_db()
