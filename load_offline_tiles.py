import tkintermapview
import os

# Specify the region to load (India)
top_left_position = (32.6407, 73.9878)  # Punjab's top-left position
bottom_right_position = (30.6821, 75.7179)  # Punjab's bottom-right position
zoom_min = 0  # Adjust the zoom levels according to your preference
zoom_max = 18

# Specify the path and name of the database
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = "offline_punjab.db"

# Create OfflineLoader instance
loader = tkintermapview.OfflineLoader(path=database_path,
                                      tile_server="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

# Save the tiles to the database, an existing database will be extended
loader.save_offline_tiles(top_left_position, bottom_right_position, zoom_min, zoom_max)

# You can call save_offline_tiles() multiple times and load multiple regions into the database.
# You can also pass a tile_server argument to the OfflineLoader and specify the server to use.
# This server needs to be then also set for the TkinterMapView when the database is used.
# You can load tiles of multiple servers in the database. Which one then will be used depends on
# which server is specified for the TkinterMapView.

# Print all regions that were loaded in the database
loader.print_loaded_sections()
