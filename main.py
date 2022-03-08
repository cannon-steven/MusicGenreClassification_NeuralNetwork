from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from tensorflow import keras


# SECTION: The Team's file imports
import loadAndPredict
from data_array import cnn_data_array, make_genres_dict, check_for_duplicates

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
    # THIS ARRAY NEEDS TO COME FROM THE MODEL
    array_from_cnn_model = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(cnn_data_array)
    if check_for_duplicates(cnn_data_array, file.filename):
        print('Cant upload same file twice')
        content = get_songs()
        render_template('main.html', content)
    data = {
                "filename": '{}'.format(file.filename),
                "genre": make_genres_dict(array_from_cnn_model)
            }
    cnn_data_array.append(data)
    content = get_songs()
    return render_template('main.html',
                           **content)


# --- TESTING STUBS ---
def predict_genre(file):
    model = keras.models.load_model("my_model")

    prediction = loadAndPredict.predict(model, file)
    return prediction


def get_songs():
    # Make a feature that will save data
    # in the state of the application while the server is running.
    return {
        "songs": cnn_data_array
    }


if __name__ == '__main__':
    app.run(debug=True)
