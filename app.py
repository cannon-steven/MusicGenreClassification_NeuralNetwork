from flask import Flask
from flask import render_template


app = Flask(__name__)

# --- WEB PAGES ---


@app.route("/", methods=["GET"])
def start():
    return render_template('start.html')


# --- BACKEND API ---
@app.route("/songs", methods=["POST"])
def songs():
    return "Nothing"
