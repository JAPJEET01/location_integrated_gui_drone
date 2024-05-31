import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
cred = credentials.Certificate("rpigps-229ad-firebase-adminsdk-88p3l-c6b5f0113f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpigps-229ad-default-rtdb.firebaseio.com/'
})

root_ref = db.reference('/')

# Delete all data from the database
root_ref.delete()
print("All data deleted from Firebase database.")


# Initialize Serial Port
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change 'COM1' to your serial port
count = 0
# Main loop to read data from serial and send to Firebase
while True:
    try:
        # Read data from serial
        data = ser.readline().decode().strip()
        
        # Send data to Firebase
        ref = db.reference('/data')
        ref.push(data)
        # print(len(data))
        
        print("Data sent to Firebase:", data)
    except KeyboardInterrupt:
        print("Exiting program")
        break
    except Exception as e:
        print("Error:", e)

# Close Serial Port
ser.close()

