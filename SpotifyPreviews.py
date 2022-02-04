import requests
import base64

# Information about client credential flow here (2 lines):
# https://developer.spotify.com/documentation/general/guides/authorization/
# client-credentials/

# Also found this article helpful:
# https://prettystatic.com/automate-the-spotify-api-with-python/

# Given when registered with spotify developer API
CLIENT_ID = "d8d312f35e424b11857344f323971ad6"
CLIENT_SECRET = "7924f51c9b7748b383b6359ae325d23b"

# URL to get developer key
AUTH_URL = "https://accounts.spotify.com/api/token"
# Primary API URL
API_URL = "https://api.spotify.com/v1"

# --- GET DEVELOPER KEY ---
# Getting a developer key requires sending this information encoded as base64
b64Message = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64Message = b64Message.encode('ascii')
b64Message = base64.b64encode(b64Message)
b64Message = b64Message.decode('ascii')

# Headers for request to get developer key
authHeaders = {
    "Authorization": f"Basic {b64Message}",
}

# Content of request to get developer key
authData = {
    "grant_type": "client_credentials"
}

# Send request for developer key
authRequest = \
    requests.post(
        AUTH_URL,
        headers=authHeaders,
        data=authData
    )

# Get developer key from response
token = authRequest.json()['access_token']


# --- GET SONGS ---
# I just have some example data here. Need to flesh this out.

# A song ID on spotify. TODO: Add way to get random track IDs
trackID = "2TpxZ7JUBn3uw46aR7qd6V"

# Set request header to include developer key
headers = {
    'Authorization': f"Bearer {token}"
}

# Send request
trackResponse = requests.get(f"{API_URL}/tracks/{trackID}", headers=headers)

# Get 30 second song preview URL from the response
preview_url = trackResponse.json()["preview_url"]

# Request the 30 second preview
previewResponse = requests.get(preview_url)

# Save song as mp3 file
# TODO: Add naming scheme for multiple files
# TODO: Convert mp3 to wav
with open("track.mp3", "wb") as f:
    f.write(previewResponse.content)
