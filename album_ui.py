import streamlit as st
import io
import album_manager
from PIL import Image

def render_album_ui(user_email):
    st.header("📚 Photo Albums")
    
    # --- Create New Album ---
    with st.expander("➕ Create New Album"):
        with st.form("new_album_form"):
            new_album_name = st.text_input("Album Name")
            new_album_desc = st.text_area("Description")
            submitted = st.form_submit_button("Create Album")
            
            if submitted and new_album_name:
                album_manager.create_album(new_album_name, new_album_desc, user_email)
                st.success(f"Album '{new_album_name}' created!")
                st.rerun()

    # --- Select Album ---
    albums = album_manager.get_all_albums()
    
    if not albums:
        st.info("No albums yet. Create one above! 👆")
        return

    # Create a dictionary for the selectbox: Name -> ID
    album_options = {album['name']: album['id'] for album in albums}
    selected_album_name = st.selectbox("Select Album", list(album_options.keys()))
    selected_album_id = album_options[selected_album_name]
    
    # --- Upload Photos to Selected Album ---
    st.subheader(f"Photos in '{selected_album_name}'")
    
    uploaded_files = st.file_uploader(
        "Add photos to this album", 
        type=['png', 'jpg', 'jpeg'], 
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Upload Photos ⬆️"):
        progress_bar = st.progress(0)
        for i, file in enumerate(uploaded_files):
            album_manager.upload_photo(selected_album_id, file, user_email)
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        st.success("Photos uploaded successfully! 🎉")
        st.rerun()

    # --- Display Photos ---
    photos = album_manager.get_photos_by_album(selected_album_id)
    
    if photos:
        # Gallery Grid
        cols = st.columns(3)
        for idx, photo in enumerate(photos):
            photo_data = album_manager.get_photo_data(photo['id'])
            if photo_data:
                # Convert memoryview/bytes to image
                image = Image.open(io.BytesIO(photo_data))
                
                with cols[idx % 3]:
                    st.image(image, use_column_width=True)
                    st.caption(f"Uploaded by {photo.get('uploaded_by', 'Unknown').split('@')[0]}")
    else:
        st.info("This album is empty. Add some memories! 📸")
