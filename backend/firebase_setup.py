import firebase_admin
from firebase_admin import credentials, firestore, storage

# NOTE: Replace with your actual Firebase Service Account path relative to backend folder
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"

def initialize_firebase():
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        # Add your storage bucket here if required or set it globally
        firebase_admin.initialize_app(cred, {
            'storageBucket': '<YOUR_PROJECT_ID>.appspot.com'
        })
        print("Firebase Admin successfully initialized.")
    except FileNotFoundError:
        print(f"Warning: Firebase credentials not found at {SERVICE_ACCOUNT_PATH}")
    except Exception as e:
        print(f"Firebase initialization error: {e}")

def get_db():
    try:
        return firestore.client()
    except Exception:
        return None

def get_storage_bucket():
    try:
        return storage.bucket()
    except Exception:
        return None
