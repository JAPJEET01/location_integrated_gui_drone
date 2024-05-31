import tkinter
import os
from tkintermapview import TkinterMapView
import threading
import time
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

datu = []
a = 0
b = 0

# Initialize Firebase
cred = credentials.Certificate("rpigps-229ad-firebase-adminsdk-88p3l-c6b5f0113f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpigps-229ad-default-rtdb.firebaseio.com/'
})

# Reference to the database
ref = db.reference('/data')


# Listen for changes on the /data reference
def handle_change(event):
    global datu, a, b, lat, lon
    data = event.data
    
    if len(data) == 21:  # Assuming data is a string with length 19
        datu = data.split(",")
        a = float(datu[0])  # Convert to float if necessary
        b = float(datu[1])  # Convert to float if necessary
        lat = a
        lon = b
        print("Updated values:", lat, lon)  # Print updated values here


ref.listen(handle_change)


# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# path for the database to use
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_punjab.db")

# create map widget and only use the tiles from the database, not the online server (use_database_only=True)
map_widget = TkinterMapView(root_tk, width=1000, height=700, corner_radius=0, use_database_only=False,
                            max_zoom=17, database_path=database_path)
map_widget.pack(fill="both", expand=True)
map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")


def marker_click(marker):
    print(f"marker clicked - text: {marker.text}  position: f'{lat, lon}'")


# define variables for latitude and longitude
lat = 31.2831274
lon = 75.6465185
prev_marker = None  # Store the reference to the previous marker


count = 0 
# def add_marker_periodically():
#     global lat, lon, prev_marker , count
#     while True:
#         if(lat != 31.2831274 ):
#         # set a position marker with updated latitude and longitude
#             marker = map_widget.set_marker(lat, lon, text= f"{count}", command=marker_click)
#             if prev_marker:
#                 # Draw a line between the current marker and the previous one
#                 path = map_widget.set_path([(prev_marker.position), marker.position])
#             prev_marker = marker
#          #   lat += 0.01  # Example increment for latitude
#          #   lon += 0.01  # Example increment for longitude#
#             #lat += random.randint(0, 9) * 0.1
#             #lon += random.randint(0, 9) * 0.1
#             time.sleep(4)  # Wait for 4 seconds before adding the next ref.listen(handle_change)
#             count+=1



# def add_marker_periodically():
#     global lat, lon, prev_marker, live_location_marker, count
#     live_location_marker = None  # Initialize the variable for the live location marker
    
#     while True:
#         if lat != 31.2831274:
#             # If the live location marker does not exist, create it
#             if live_location_marker is None:
#                 live_location_marker = map_widget.set_marker(lat, lon, text=f"live location", command=marker_click)
#             else:
#                 # Update the position of the existing live location marker
#                 live_location_marker.set_position(lat, lon)
            
#             # Increment the count for the marker text (optional)
#             count += 1
            
#             # Pause for a moment before updating the location again
#             time.sleep(4)


def add_marker_periodically():
    global lat, lon, live_location_marker, count

    # Initialize the live location marker to None initially
    live_location_marker = None
    
    map_widget.set_zoom(19)  # Adjust the zoom level to your desired level (e.g., 15)
    while True:
        if lat != 31.2831274:
            # If the live location marker does not exist, create it
            if live_location_marker is None:
                live_location_marker = map_widget.set_marker(lat, lon, text=f"live location", command=marker_click)
            # else:
                # Update the position of the existing live location marker
                live_location_marker.set_position(lat, lon)
            
            # Center the map on the live location and set zoom level
            map_widget.set_position(lat, lon)  # Center the map on the live location

            # Increment the count for the marker text (optional)
            count += 1
            
            # Pause for a moment before updating the location again
            time.sleep(4)


# Start a separate thread to add markers periodically
marker_thread = threading.Thread(target=add_marker_periodically)
marker_thread.daemon = True
marker_thread.start()

root_tk.mainloop()
