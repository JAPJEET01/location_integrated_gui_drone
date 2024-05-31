import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
cred = credentials.Certificate("rpigps-229ad-firebase-adminsdk-88p3l-c6b5f0113f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpigps-229ad-default-rtdb.firebaseio.com/'
})

# Reference to the database
ref = db.reference('/data')
root_ref = db.reference('/')

# Delete all data from the database
root_ref.delete()
print('previous data deleted')

# Listen for changes on the /data reference
def handle_change(event):
    if len(event.data) == 21:
        return  event.data

ref.listen(handle_change)
