import sys
import Spotify_API_utilities as sp

# Creates a .csv file filled with feature data extracted from song clips on
# Spotify. Quantity is the number of songs in each genre you would like to add
# to the file.

# Verify presence of quantity argument
if len(sys.argv) != 2:
    print("Usage: create_dataset.py <quantity>")
    sys.exit()

quantity = int(sys.argv[1])

genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal",
          "pop", "reggae", "rock"]
sp.collect_spotify_data(genres, quantity)
