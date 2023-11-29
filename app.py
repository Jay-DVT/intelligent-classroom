from flask import Flask, render_template, jsonify, request, redirect, url_for
from runner import *
from pdf_handler import clean_local

app = Flask(__name__)

# Global variable to keep track of the current slide and music state
total_slides = 10  # Total number of slides
music_playing = False  # State of the music


@app.route('/')
def home():
    clean_local()
    classes = search_available_classes()
    return render_template('home.html', classes=classes)


@app.route('/presentation/<serial>', methods=['POST'])
def presentation(serial):
    global current_slide, total_slides
    current_slide = 1
    information = setup_class(serial)
    total_slides = information['total_slides']
    return render_template('presentation.html', serial=serial, slide=current_slide)


@app.route('/change_slide', methods=['POST'])
def change_slide():
    global current_slide, total_slides
    current_slide += 1
    if current_slide > total_slides:
        return redirect(url_for('home'))
    return jsonify({'slide': current_slide})


@app.route('/current_slide')
def current_slide():
    global current_slide
    return jsonify({'slide': current_slide})


@app.route('/toggle_music', methods=['POST'])
def toggle_music():
    global music_playing
    music_playing = not music_playing
    return jsonify({'music_playing': music_playing})


if __name__ == '__main__':
    app.run(debug=True)
