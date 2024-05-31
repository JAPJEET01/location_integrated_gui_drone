import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key file
service_account_key_path = 'rpigps-229ad-firebase-adminsdk-88p3l-c6b5f0113f.json'

# Initialize the Firebase app with the service account key
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpigps-229ad-default-rtdb.firebaseio.com/'
})

# Reference to the root of your database
# Reference to the root of your database
root_ref = db.reference('/')

# Delete all data from the database
root_ref.delete()

print("All data deleted from Firebase database.")