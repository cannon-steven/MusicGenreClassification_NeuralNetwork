import requests
import base64
import random

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
def get_developer_key():
    # Getting a developer key requires sending this info encoded as base64
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

    return token


TOKEN = get_developer_key()


# --- GET SONGS ---
# https://perryjanssen.medium.com/getting-random-tracks-using-the-spotify
# -api-61889b0c0c27      (link is both lines)
def gen_rand_track_string():
    """
    Generates a random string of the form 'a%'. Spotify search api can take
    a wildcard character "%" and return all matching items
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    letter = random.choice(alphabet)

    return f"{letter}%"


def get_random_track(genre):
    """
    Calls the Spotify API to get the name and spotify ID for a random song
    """
    # Get a random song to search for
    rand_string = gen_rand_track_string()

    # Query Parameters at end of URL: ?q=songname&type=track   etc.
    queryParams = {
        "q": rand_string,
        "type": "track",
        "offset": random.randint(0, 999),
        "limit": 1
    }

    # Send API key in HTTP header
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    # Get track data from Spotify API
    trackData = requests.get(
        f"{API_URL}/search",
        params=queryParams,
        headers=headers
    )

    # Parse response for Name and ID
    trackName = trackData.json()["tracks"]["items"][0]["name"]
    trackID = trackData.json()["tracks"]["items"][0]["id"]

    return {"trackName": trackName, "trackID": trackID}


get_random_track()

# A song ID on spotify. TODO: Add way to get random track IDs
# trackID = "2TpxZ7JUBn3uw46aR7qd6V"

# Set request header to include developer key
# headers = {
#     'Authorization': f"Bearer {token}"
# }

# # Send request
# trackResponse = requests.get(f"{API_URL}/tracks/{trackID}", headers=headers)

# # Get 30 second song preview URL from the response
# preview_url = trackResponse.json()["preview_url"]

# # Request the 30 second preview
# previewResponse = requests.get(preview_url)

# # Save song as mp3 file
# # TODO: Add naming scheme for multiple files
# # TODO: Convert mp3 to wav
# with open("track.mp3", "wb") as f:
#     f.write(previewResponse.content)
