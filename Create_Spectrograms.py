import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os


def build_empty_directories(outputDirectory, labels):
    """
    Creates a set of empty directories in the cwd for filling with data.
    Returns the path to the container directory holding the sub-directories
    """
    os.mkdir(outputDirectory)
    for label in labels:
        os.mkdir(f"{outputDirectory}/{label}")


def parse_file_name(path):
    """Given a path like './directory/file.txt' returns the file name 'file'"""
    file = path[path.rfind('/') + 1:path.rfind('.')]
    return file


def parse_directory(path):
    """
    Given a path like './directory/subdirectory' returns the final directory
    'subdirectory'
    """
    directoryStr = path[path.rfind('/') + 1:]
    return directoryStr


def save_spectrogram(songPath, destination):
    """
    Given the path to a .wav file and a destination directory, saves a png
    image of the spectrogram to the directory
    """
    # Get filename
    filename = parse_file_name(songPath)
    filename += ".png"

    # Get song representation as a spectrogram
    y, sr = librosa.load(songPath)
    data = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(data), ref=np.max)
    librosa.display.specshow(S_db)

    # Save file to destination
    plt.savefig(f"{destination}/{filename}")


def generate_spectrograms(inputDirectory, outputDirectory):
    """
    Given the GTZAN genres dataset, creates spectrograms and fills a
    training directory
    """
    # Get list of genres
    genres = os.listdir(inputDirectory)

    # Create empty directories to put the spectrograms into
    dirName = parse_directory(outputDirectory)
    if dirName not in os.listdir("./"):
        build_empty_directories(outputDirectory, genres)

    # Get songs and convert them to spectrograms
    for genre in genres:
        for song in os.listdir(f"{inputDirectory}/{genre}"):
            file_png = parse_file_name(song) + ".png"
            if file_png not in os.listdir(f"{outputDirectory}/{genre}"):
                print(f"Generating spectrogram for {song}")
                save_spectrogram(f"{inputDirectory}/{genre}/{song}",
                                 f"{outputDirectory}/{genre}")


generate_spectrograms("./Data/genres_original", "./Spectrograms")
