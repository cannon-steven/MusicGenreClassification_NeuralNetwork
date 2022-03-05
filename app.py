from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from tensorflow import keras
import json
import loadAndPredict
import os
from werkzeug.utils import secure_filename
import tempfile

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# We should set the maximum content length
# (you can check your .wav file size with
# ls -lh songname.wav):
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


# --- HELPER FUNCTIONS ---
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
def is_allowed_file(filename):
    """Returns True/False if a given file ends with an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getMax(dict):
    """Finds the element in a dictionary whose value is the greatest"""
    max = None
    for element in dict:
        if max is None or dict[element] > dict[max]:
            max = element
    return max


# --- WEB PAGES ---
@app.route("/")
def start():
    return render_template('start.html')


@app.route("/main")
@cross_origin()
def main_web_page():
    content = get_songs()
    for song in content['songs']:
        song['primaryGenre'] = getMax(song['genre'])
    print(content['songs'])
    return render_template('main.html', **content)
    # The ** operator turns a dictionary into keyword arguments.
    # {'example': 'data', 'ex2': 'data'} -> example='data', ex2='data'


# --- BACKEND API ---
@app.route("/songs", methods=["POST"])
@cross_origin()
def upload_song():
    # Check that a file is present
    if 'file' not in request.files:
        return {"error":    "No file, or form input unnamed."
                            + " Expected a .wav file input named 'file'"
                }, 400

    # Verify file extension
    file = request.files["file"]
    if not is_allowed_file(file.filename):  # file.filename = "example.wav"
        return {"error": "Expected a .wav file"}, 400

    # make a temporary directory where you can save uploaded files
    temp_dir = tempfile.TemporaryDirectory()
    # make sure the file is not wrapped in the fileStorage class
    # before sending it to the predict_genre
    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(temp_dir.name, filename))
    # Get the data from here
    # genreResults = predict_genre(f'{temp_dir.name}/{filename}')
    # delete the temporary file
    temp_dir.cleanup()
    data = {
        "songs": [
            {
                "filename": "blues.wav",
                "genre": {
                    "blues": 61, "classical": 5, "country": 5,
                    "disco": 4, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "bad.wav",
                "genre": {
                    "blues": 60, "classical": 5, "country": 5,
                    "disco": 5, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "thriller.wav",
                "genre": {
                    "blues": 65, "classical": 5, "country": 5,
                    "disco": 0, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            }
        ]
    }
    return render_template('main.html',
                           songs=json.dumps(data))


# --- TESTING STUBS ---
def predict_genre(file):
    model = keras.models.load_model("my_model")

    prediction = loadAndPredict.predict(model, file)
    return prediction


def get_songs():
    # Get the data from a text file
    return {
        "songs": [
            {
                "filename": "blues.wav",
                "genre": {
                    "blues": 61, "classical": 5, "country": 5,
                    "disco": 4, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "bad.wav",
                "genre": {
                    "blues": 60, "classical": 5, "country": 5,
                    "disco": 5, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "thriller.wav",
                "genre": {
                    "blues": 65, "classical": 5, "country": 5,
                    "disco": 0, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "hello.wav",
                "genre": {
                    "blues": 65, "classical": 5, "country": 5,
                    "disco": 0, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            }
        ]
    }


if __name__ == '__main__':
    app.run(debug=True)
