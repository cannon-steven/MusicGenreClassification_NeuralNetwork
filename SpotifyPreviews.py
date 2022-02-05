import requests
import base64
import random
import soundfile as sf

# Information about client credential flow here (2 lines):
# https://developer.spotify.com/documentation/general/guides/authorization/
# client-credentials/

# Also found this article helpful:
# https://prettystatic.com/automate-the-spotify-api-with-python/

# Given when registered with spotify developer API
# TODO: THESE SHOULD BE MOVED TO .env
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


# API keys expire, so it is helpful to generate new ones each time
TOKEN = get_developer_key()


# --- GET SONGS ---
def get_genres():
    """
    Requests genres from the spotify API and returns a list of available genres
    """
    # Send API key in HTTP header
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    genreData = requests.get(
        f"{API_URL}/recommendations/available-genre-seeds",
        headers=headers
    )

    return genreData.json()["genres"]


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
    Calls the Spotify API to get the name and spotify ID for a random song in a
    specific genre
    """
    # Get a random song to search for
    rand_string = gen_rand_track_string()

    # Query Parameters at end of URL: ?q=songname&type=track   etc.
    # genre has to be part of q instead of own parameter
    # https://developer.spotify.com/documentation/web-api/reference/#/
    # operations/search   (2 lines)
    queryParams = {
        "q": f"{rand_string} genre:{genre}",
        "type": "track",
        "offset": random.randint(0, 999),
        "limit": 10
    }

    # Send API key in HTTP header
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
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

    except:
        return {
            "error": "Something went wrong with the request." +
                     "It is likely the genre was not recognized"}


exTrackID = "0oPdaY4dXtc3ZsaG17V972"  # TODO: FOR TESTING - REMOVE THIS


def get_preview_URL(trackID):
    """
    Given the spotify ID of a track, returns the URL for a 30 second preview
    """
    # Set request header to include developer key
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    # Send request
    trackData = requests.get(
        f"{API_URL}/tracks/{trackID}", 
        headers=headers
    )

    # Get 30 second song preview URL from the response
    previewURL = trackData.json()["preview_url"]

    return previewURL


def get_wav(preview_URL):
    """
    Given a spotify preview URL, returns a .wav file
    """


def extract_features(wavFile):
    """
    Given a .wav file, extracts the data necessary to process the song through
    the Convolutional Neural Network model. Returns the data as a dictionary
    {
        chroma_stft: data,
        rmse: data,
        spectral_centroid: data,
        spectral_bandwidth: data,
        rolloff: data,
        zero_crossing_rate: data,
        mfcc1: data,
        ...
        mfcc20: data
    }
    """
    features = dict()


def format_csvData(name, featureData, label):
    """
    Formats data into a string to be added to a CSV file.

    Format: "filename,chroma_stft,rmse,spectral_centroid,
    spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,...,mfcc20,label"
    """
    mfccString = ""
    for i in range(1, 21):  # mfcc1 to mfcc20
        mfccString.append(featureData[f"mfcc{i},"])

    csvString = f"{name}"\
                + f"{featureData['chroma_stft']},"\
                + f"{featureData['rmse']},"\
                + f"{featureData['spectral_centroid']},"\
                + f"{featureData['spectral_bandwidth']},"\
                + f"{featureData['rolloff']},"\
                + f"{featureData['zero_crossing_rate']},"\
                + f"{mfccString}"\
                + f"{label}"

    return csvString


def append_data(dataString, csvFile="song_data.csv"):
    """
    Given a string, appends it to the end of a csv file.

    expected format: "filename,chroma_stft,rmse,spectral_centroid,
    spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,...,mfcc20,label"
    """

# # print(get_preview_URL(exTrackID))
    
# # Request the 30 second preview
# previewResponse = requests.get("https://p.scdn.co/mp3-preview/5bd22befb5bd4b407a3a4de2a5947a1fb3d53ff6?cid=d8d312f35e424b11857344f323971ad6")

# # Save song as mp3 file
# # TODO: Add naming scheme for multiple files
# # TODO: Convert mp3 to wav
# with open("FelizNavidad.mp3", "wb") as f:
#     f.write(previewResponse.content)
