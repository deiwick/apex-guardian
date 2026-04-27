import os
import tempfile
import cv2
import firebase_admin
from firebase_admin import firestore, storage as admin_storage
from firebase_functions import storage_fn
import google.generativeai as genai
from perception.hashers import PHash

# Initialize Firebase Admin SDK
firebase_admin.initialize_app()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBldI6DpbXw465rQk9ULt7SWAdkO47RDY8")
genai.configure(api_key=GENAI_API_KEY)

@storage_fn.on_object_finalized()
def process_official_media(event: storage_fn.CloudEvent[storage_fn.StorageObjectData]):
    """Cloud Function triggered upon file upload to Firebase Storage."""
    bucket_name = event.data.bucket
    file_path = event.data.name
    
    # 1. Verification of the 'official_assets' folder constraint
    if not file_path.startswith("official_assets/"):
        print(f"File {file_path} ignored: Not in official_assets/")
        return
        
    print(f"Processing newly uploaded official asset: {file_path}")
    
    # Setup temporary files for processing
    ext = file_path.split('.')[-1] if '.' in file_path else 'mp4'
    _, temp_local_filename = tempfile.mkstemp(suffix=f".{ext}")
    frame_path = temp_local_filename + "_frame.jpg"
    
    try:
        # 2. Download the file from Firebase Storage
        bucket = admin_storage.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.download_to_filename(temp_local_filename)
        
        # 3. pHash generation using 'perception' library
        # We capture the very first frame to create a stable hash representing this asset.
        vidcap = cv2.VideoCapture(temp_local_filename)
        success, image_cv = vidcap.read()
        
        phash_val = "UNAVAILABLE"
        if success:
            # Save the frame to be natively computed by the perception library
            cv2.imwrite(frame_path, image_cv)
            
            # Using the PHash algorithm from perception
            hasher = PHash()
            phash_val = hasher.compute(frame_path)
        else:
            print("Warning: Could not extract frame for pHash generation.")
            
        # 4. Describe video content using Gemini (Flash Model)
        # Using the File API for robust media handling
        print("Uploading to Gemini File API...")
        media_file = genai.upload_file(path=temp_local_filename)
        
        model = genai.GenerativeModel(model_name="gemini-1.5-flash") # The Flash model family
        prompt = "You are a sports analyst. Describe the video's content briefly in a single descriptive sentence. (e.g., 'A goal by Messi', 'A slam dunk by LeBron', etc.)"
        
        print("Generating description...")
        response = model.generate_content([prompt, media_file])
        description = response.text.strip()
        
        print(f"Generated Description: {description}")
        print(f"Generated pHash: {phash_val}")
        
        # Cleanup Gemini File API to prevent storage buildup
        try:
            genai.delete_file(media_file.name)
        except Exception as e:
            print(f"Warning: Failed to cleanup Gemini file {media_file.name}: {e}")
            
        # 5. Save the data into Firestore 'registered_assets'
        db = firestore.client()
        doc_ref = db.collection("registered_assets").document()
        doc_ref.set({
            "storage_path": file_path,
            "phash": str(phash_val),
            "description": description,
            "bucket": bucket_name
        })
        
        print(f"Successfully processed and stored record for {file_path}")
        
    except Exception as e:
        print(f"Runtime Exception during processing: {e}")
        
    finally:
        # 6. Cleanup local execution environment
        if os.path.exists(temp_local_filename):
            os.remove(temp_local_filename)
        if os.path.exists(frame_path):
            os.remove(frame_path)
