import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from runner import *
from pdf_handler import clean_local

load_dotenv()

COMPONENTS_API_ADDRESS = os.environ.get('COMPONENTS_API_ADDRESS')
WORKING_PATH = os.environ.get('WORKING_PATH')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app)

# Global variable to keep track of the current slide and music state
total_slides = 0            # Total number of slides
music_playing = False       # State of the music
current_slide = 1           # Current slide number
presentation_serial = ''    # Serial number of the presentation
presentating = False        # State of the presentation


@app.route('/')
def home():
    clean_local()
    global presentating
    presentating = False
    classes = search_available_classes()
    return render_template('home.html', classes=classes)


@app.route('/presentation/<serial>', methods=['POST'])
def presentation(serial):
    global current_slide, total_slides, presentation_serial, presentating
    presentating = True
    current_slide = 1
    presentation_serial = serial
    information = setup_class(serial)
    run_instructions(serial, 1)
    total_slides = information['total_slides']
    return render_template('presentation.html', serial=serial, slide=current_slide)


@socketio.on('change_slide')
def handle_change_slide(message):
    global current_slide, total_slides, presentation_serial, presentating
    if message['action'] == 'next' and presentating:
        current_slide += 1
        if current_slide > total_slides:
            current_slide = 1
            emit('redirect_home', broadcast=True)
        else:
            run_instructions(presentation_serial, current_slide)
            emit('update_slide', {'slide': current_slide}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
