from flask import Flask, request, Response, render_template, jsonify

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

