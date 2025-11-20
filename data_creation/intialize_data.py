import firebase_admin
from firebase_admin import credentials, firestore

db = None

def initialize_firebase():
    global db
    
    if db is not None:
        return db
        
    try:
        cred = credentials.Certificate(r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\recipethinkbridge-firebase.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Firebase initialized successfully.")
        return db
        
    except FileNotFoundError:
        print(f"Error: Service Account Key not found at")
        print("Please ensure 'serviceAccountKey.json' is in the project root.")
        return None
    except Exception as e:
        print(f" An error occurred during Firebase initialization: {e}")
        return None

initialize_firebase()