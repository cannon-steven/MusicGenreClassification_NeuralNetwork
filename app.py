from flask import Flask, request, Response, render_template
import json

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)


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
def main_web_page():
    content = get_songs()
    for song in content['songs']:
        song['primaryGenre'] = getMax(song['genre'])
    return render_template('main.html', **content)
    # The ** operator turns a dictionary into keyword arguments.
    # {'example': 'data', 'ex2': 'data'} -> example='data', ex2='data'


# --- BACKEND API ---
@app.route("/songs", methods=["POST"])
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

    # Send file to the model
    genreResults = predict_genre(file)

    return Response(
                    response=json.dumps({
                                        "filename": file.filename,
                                        "genre": genreResults
                                        }),
                    status=201,  # Maybe use 202? Depends on processing time
                    content_type="application/json"
                    )


# --- TESTING STUBS ---
def predict_genre(file):
    return {"rock": 80, "pop": 20}


def get_songs():
    return {
        "songs": [
            {
                "filename": "beat_it.wav",
                "genre": {
                    "rock": 80,
                    "pop": 20
                }
            },
            {
                "filename": "bad.wav",
                "genre": {
                    "rock": 75,
                    "pop": 25
                }
            },
            {
                "filename": "thriller.wav",
                "genre": {
                    "rock": 80,
                    "pop": 20,
                    "spooks": 100
                }
            }
        ]
    }
