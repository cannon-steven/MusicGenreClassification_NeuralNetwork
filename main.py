from flask import Flask, request, render_template
import tempfile
import os
from werkzeug.utils import secure_filename
# SECTION: The Team's file import
from dataArrayModel import cnn_data_array, make_genres_dict
from dataArrayModel import check_for_duplicates
from loadAndPredict import makePrediction
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)

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
                            + " Expected a .mp3 file input named 'file'"
                }, 400

    # Verify file extension
    file = request.files["file"]
    if not is_allowed_file(file.filename):  # file.filename = "example.wav"
        return {"error": "Expected a .mp3 file"}, 400

    # Make a temporary directory where you can save uploaded files
    temp_dir = tempfile.TemporaryDirectory()
    # make sure the file is not wrapped in the fileStorage class
    # before sending it to the predict_genre
    filename = secure_filename(file.filename)
    file.save(os.path.join(temp_dir.name, filename))

    # SECTION: arr_data calls makePrediction
    # with the filename of the uploaded file
    arr_data = makePrediction(f'{temp_dir.name}/{filename}')
    array_from_cnn_model = list(map(lambda x: int(x*100), arr_data))
    # Check for duplicate uploads
    if check_for_duplicates(cnn_data_array, f'{filename}'):
        content = get_songs()
        return render_template('main.html', **content)
    # Make the new data structure to append to array
    data = {
                "filename": '{}'.format(f'{filename}'),
                "genre": make_genres_dict(array_from_cnn_model)
            }
    cnn_data_array.append(data)
    content = get_songs()
    # Add the primary Genre to the data structure
    # and render the template with the new data structure
    for song in content['songs']:
        song['primaryGenre'] = getMax(song['genre'])
    return render_template('main.html',
                           **content)


def get_songs():
    # Make a feature that will save data
    # in the state of the application while the server is running.
    return {
        "songs": cnn_data_array
    }


if __name__ == '__main__':
    app.run(debug=True)
