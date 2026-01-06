import psycopg2
from db_config import execute_query, get_db_connection

def create_album(name, description, user_email):
    """Create a new photo album."""
    query = """
    INSERT INTO albums (name, description, created_by)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(query, (name, description, user_email))
        album_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return album_id
    except Exception as e:
        print(f"Error creating album: {e}")
        if conn:
            conn.close()
        return None

def get_all_albums():
    """Retrieve all albums."""
    query = "SELECT * FROM albums ORDER BY created_at DESC;"
    return execute_query(query, fetch=True)

def upload_photo(album_id, file_obj, user_email):
    """Upload a photo to an album."""
    query = """
    INSERT INTO photos (album_id, filename, image_data, uploaded_by)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """
    
    # Read file binary data
    file_data = file_obj.read()
    binary_data = psycopg2.Binary(file_data)
    
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cur = conn.cursor()
        cur.execute(query, (album_id, file_obj.name, binary_data, user_email))
        photo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        # Reset file pointer for other uses if needed
        file_obj.seek(0)
        return photo_id
    except Exception as e:
        print(f"Error uploading photo: {e}")
        if conn:
            conn.close()
        return None

def get_photos_by_album(album_id):
    """Retrieve all photos in an album."""
    query = "SELECT id, filename, uploaded_by, uploaded_at FROM photos WHERE album_id = %s ORDER BY uploaded_at DESC;"
    return execute_query(query, (album_id,), fetch=True)

def get_photo_data(photo_id):
    """Retrieve the binary data of a specific photo."""
    query = "SELECT image_data FROM photos WHERE id = %s;"
    result = execute_query(query, (photo_id,), fetch=True)
    if result:
        return result[0]['image_data']
    return None
