import firebase_admin
from firebase_admin import credentials, firestore

# Step 1: Initialize Firebase
cred = credentials.Certificate("your-firebase-acc")  # Use your actual service account file
firebase_admin.initialize_app(cred)

# Step 2: Get Firestore client
db = firestore.client()

# Step 3: Try writing a simple test document
db.collection("bulb_data").document("test_doc").set({"test": "Hello Firestore"})

print("✅ Test document uploaded to Firestore.")
