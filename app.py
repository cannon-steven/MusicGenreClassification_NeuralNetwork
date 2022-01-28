from flask import Flask, request, Response, render_template
import json

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)


# --- HELPER FUNCTIONS ---
def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- WEB PAGES ---
@app.route("/")
def start():
    return render_template('start.html')


@app.route("/main")
def main_web_page():
    return render_template('main.html')


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


# --- Testing Stubs ---
def predict_genre(file):
    return {"rock": 80, "pop": 20}


def get_songs():
    return [
        {
            "filename": "beat_it.mp3",
            "genre": {
                "rock": 80,
                "pop": 20
            }
        },
        {
            "filename": "beat_it.mp3",
            "genre": {
                "rock": 80,
                "pop": 20
            }
        },
        {
            "filename": "beat_it.mp3",
            "genre": {
                "rock": 80,
                "pop": 20
            }
        }
    ]
