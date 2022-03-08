# MusicGenreClassification_NeuralNetwork

## N-Music Neural Network Website


### Objective

* Build dataset containing song metadata, and their various genres, and spectrograph information.
* Develop a pipeline to import audio clips from datasets.
* Train a CNN or other neural network to predict music genres from a curated dataset.
* Develop a program to run a user-submitted audio clip against the model and print results with accuracy metric.

### Scope

This project will focus on:
* Keras and Tensorflow to: train, test, and validate neural networks
* Librosa for audio preprocessing and manipulation
* Matplotlib: data analysis and visualization
* Numpy and Pandas: data structures and utilify functions
* YouTube-dl: to obtain the audio files for the training dataset


### Basic Requirements

* The user will enter a song clip
* User will then receive a formatted top-n list of genres 
* the list of genres will be sorted by confidence value in descending order.


### Stretch Goals

* Create a web app front-end (can run on desktop).
* Host the program as a web server.
* Content based recommender system for music similar to audio clip

#### Technical Constraints

* Use Tensorflow and Keras


### Instructions

* Fork this repository (do not clone) to your own GitHub account.

### Installation Instructions 

* Please make sure you have a python ^3.9.0 version and up.
* For ways to download Python to different operating systems, please refer to the official guides: https://www.python.org/downloads/
* Once you have python3 installed:
* You can clone the repo or fork it:
#### To clone:
* git clone https://github.com/cannon-steven/MusicGenreClassification_NeuralNetwork.git give_a_project_name

#### To install dependencies/requirements
* pip install -r requirements.txt

#### To run the Flask server
* export FLASK_APP=give_a_project_name
* flask run


#### You will see the server running on your terminal and can open the link to view the project.

### Resources 
###### Feel free to add any good resources on Tensorflow and Keras

* [Top-n Music Project Proposal](https://eecs.oregonstate.edu/capstone/submission/pages/viewSingleProject.php?id=Si8d04xsueSfU0id)
* [Musical Genre Classification of Audio Signals](https://ieeexplore.ieee.org/document/1021072)
