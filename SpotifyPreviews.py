import requests
import base64
import random
import librosa
import numpy as np
import os
import sys
from pydub import AudioSegment

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

CSV_HEADERS = "filename,chroma_stft,rmse,spectral_centroid,"\
            + "spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,mfcc2,"\
            + "mfcc3,mfcc4,mfcc5,mfcc6,mfcc7,mfcc8,mfcc9,mfcc10,mfcc11,"\
            + "mfcc12,mfcc13,mfcc14,mfcc15,mfcc16,mfcc17,mfcc18,mfcc19,"\
            + "mfcc20,label"


# --- GET DEVELOPER KEY ---
def get_developer_key():
    """
    Get a developer API key from spotify. Required for accessing most of the
    API. API keys expire, so a periodic renewal is necessary
    """
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


# --- GET SONGS ---
def get_genres(apiKey):
    """
    Requests genres from the spotify API and returns a list of available genres
    """
    # Send API key in HTTP header
    headers = {
        "Authorization": f"Bearer {apiKey}"
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


def get_random_trackID(genre, apiKey):
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
        "Authorization": f"Bearer {apiKey}"
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
        return {"error": "Something went wrong with the request."}


def get_preview_URL(trackID, apiKey):
    """
    Given the spotify ID of a track, returns the URL for a 30 second preview
    """
    # Set request header to include developer key
    headers = {
        'Authorization': f"Bearer {apiKey}"
    }
    # Send request
    trackData = requests.get(
        f"{API_URL}/tracks/{trackID}",
        headers=headers
    )

    # Get 30 second song preview URL from the response
    preview_url = trackData.json()["preview_url"]

    return preview_url


def mp3_to_wav(mp3FilePath):
    """
    Given the path to an .mp3 file, creates a .wav copy and returns the path to
    the copy
    """
    # Get file path as .wav
    wavFilePath = f"{mp3FilePath[0:-4]}.wav"

    # Copy mp3 file to wav
    sound = AudioSegment.from_mp3(mp3FilePath)
    sound.export(wavFilePath, format="wav")

    return wavFilePath


def temp_download(preview_url):
    """
    Given a spotify preview URL, downloads it as a .wav file and returns the
    path to the file
    """


def extract_features(trackFilePath):
    """
    Given the path to a .wav file, extracts the data necessary to process the
    song through the Convolutional Neural Network model.
    Returns the data as a dictionary
    {
        chroma_stft: data,
        rms: data,
        spectral_centroid: data,
        spectral_bandwidth: data,
        rolloff: data,
        zero_crossing_rate: data,
        mfcc1: data,
        ...
        mfcc20: data
    }
    """
    # Initialize feature dictionary
    features = dict()

    # Load song as audio time series array
    timeSeries, sampleRate = librosa.load(trackFilePath, duration=30)

    # Process data and store features in feature dictionary
    features["chroma_stft"] = \
        np.mean(librosa.feature.chroma_stft(y=timeSeries))
    features["rms"] = \
        np.mean(librosa.feature.rms(y=timeSeries))
    features["spectral_centroid"] = \
        np.mean(librosa.feature.spectral_centroid(y=timeSeries))
    features["spectral_bandwidth"] = \
        np.mean(librosa.feature.spectral_bandwidth(y=timeSeries))
    features["rolloff"] = \
        np.mean(librosa.feature.spectral_rolloff(y=timeSeries))
    features["zero_crossing_rate"] = \
        np.mean(librosa.feature.zero_crossing_rate(y=timeSeries))
    i = 1
    for coefficient in librosa.feature.mfcc(y=timeSeries):
        features[f"mfcc{i}"] = coefficient
        i += 1

    return features


def format_csvData(name, featureData, label):
    """
    Formats data into a string to be added to a CSV file.

    Format: "filename,chroma_stft,rms,spectral_centroid,
    spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,...,mfcc20,label"
    """
    mfccString = ""
    for i in range(1, 21):  # mfcc1 to mfcc20
        mfccString.append(featureData[f"mfcc{i},"])

    csvString = f"{name}"\
                + f"{featureData['chroma_stft']},"\
                + f"{featureData['rms']},"\
                + f"{featureData['spectral_centroid']},"\
                + f"{featureData['spectral_bandwidth']},"\
                + f"{featureData['rolloff']},"\
                + f"{featureData['zero_crossing_rate']},"\
                + f"{mfccString}"\
                + f"{label}"

    return csvString


def append_data(dataString, csvFile):
    """
    Given a string, appends it to the end of a csv file.

    expected format: "filename,chroma_stft,rms,spectral_centroid,
    spectral_bandwidth,rolloff,zero_crossing_rate,mfcc1,...,mfcc20,label"
    """
    with open(csvFile, 'a', newline="") as file:
        file.write(dataString)


def matching_headers(filepath):
    """
    Returns True/False if the given file has the expected headers
    """
    with open(filepath, "r") as file:
        if file.readline() == CSV_HEADERS:
            return True
        else:
            return False


def add_headers(filepath):
    """Adds headers to csv file. Overwrites file if not empty"""
    with open(filepath, "w") as file:
        file.write(CSV_HEADERS)


def confirm_file(filepath):
    """Check with the user that they are using the correct file"""
    if os.path.exists(filepath):
        print(f"The chosen file '{filepath}' already exists. What would you"
              + " like to do?"
              + "1. Overwrite file\n"
              + "2. Add to file\n"
              + "3. Quit\n")
        choice = 0
        while choice not in [1, 2, 3]:
            choice = int(input("Option: "))
        if choice == 1:
            add_headers(filepath)
        elif choice == 2:
            if not matching_headers(filepath):
                print("The headers for the selected file do not match. "
                      + "Would you like to continue?\n"
                      + "1. Yes\n"
                      + "2. No\n")
                choice2 = 0
                while choice2 not in [1, 2]:
                    choice2 = int(input("Option: "))
                if choice2 == 2:
                    sys.exit()
        elif choice == 3:
            sys.exit()


def get_tracksData(genre, quantity, apiKey):
    """
    genre [string]  - The genre of music to get tracks for
    quantity [int]  - The number of tracks to get.

    Returns a dictionary of tracks from spotify in the format
    {
        {
            "name": "A song",
            "preview_url": "http://someurl.com/12345"
        }
    }
    """
    # Prepare search parameters
    limit = 50
    if quantity < 50:
        limit = quantity

    queryParams = {
        "q": f"{genre}",
        "type": "track",
        "offset": 0,
        "limit": f"{limit}"
    }

    # Send API key in HTTP header
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }

    try:
        # Get track data from Spotify search API
        trackData = requests.get(
            f"{API_URL}/search",
            params=queryParams,
            headers=headers
        )
        # Parse for name and preview URL and add to list
        parsed_data = []
        for track in trackData.json()["tracks"]["items"]:
            parsed_data.append(
                {
                    "name": track["name"],
                    "preview_url": track["preview_url"]
                }
            )

        # Get next seach link (APIs typically return a limited list of items
        # along with a link to the next set)
        nextURL = trackData.json()["tracks"]["next"]

    except:
        return {"error": "Something went wrong with the request."}

    # Get more tracks until specified quantity reached TODO: Implementation
    # only works with multiples of 50. Update to accept other numbers?
    quantity -= 50
    while quantity >= 50:
        try:
            # Send API key in HTTP header
            headers = {
                "Authorization": f"Bearer {apiKey}"
            }

            # Get next set of 50 tracks
            trackData = requests.get(
                nextURL,
                headers=headers
            )
            for track in trackData.json()["tracks"]["items"]:
                parsed_data.append(
                    {
                        "name": track["name"],
                        "preview_url": track["preview_url"]
                    }
                )
            quantity -= 50

        except:
            return {"error": "Something went wrong with the request."}

    return parsed_data


def collect_spotify_data(genres, quantity, outputfile="track_features.csv"):
    """
    Gets audio clips from spotify, processes them to extract feature data, and
    appends the data to a given file.
        genres [list]   - Strings representing genres of music to get data for
        quantity [int]  - The number of songs per genre to collect data for
        file [string]   - The relative path to a csv file to store the data in

    """
    # Loop through genres and append feature data to file
    for genre in genres:
        tracksData = get_tracksData(genre, quantity)
        for track in tracksData:
            soundclip = temp_download(track["preview_url"])
            features = extract_features(soundclip)
            csvString = format_csvData(track["name"], features, genre)
            append_data(csvString, outputfile)
