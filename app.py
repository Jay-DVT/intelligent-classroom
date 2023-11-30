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
current_step = 1           # Current slide number
presentation_serial = ''    # Serial number of the presentation
presentating = False        # State of the presentation
current_delay = 1000000000  # Current delay between slides
current_slide = 1
total_steps = 0
interrupted = False


@app.route('/')
def home():
    clean_local()
    global presentating, current_slide
    presentating = False
    classes = search_available_classes()
    current_slide = 1
    return render_template('home.html', classes=classes)


@app.route('/presentation/<serial>', methods=['POST'])
def presentation(serial):
    global current_slide, total_slides, presentation_serial, presentating, current_delay, music_playing, current_step, total_steps
    presentating = True
    current_slide = 1
    presentation_serial = serial
    information = setup_class(serial)
    total_steps = information['total_steps']
    total_slides = information['total_slides']
    parameters = run_instructions(serial, 1)
    if 'Sound' in parameters:
        music_playing = parameters['Sound']
    if 'Delay' in parameters:
        current_delay = parameters['Delay']
    return render_template('presentation.html', serial=serial, slide=parameters['Screen'])


@socketio.on('change_slide')
def handle_change_slide(message):
    global current_slide, total_slides, presentation_serial, presentating, current_delay, music_playing, current_step, total_steps, interrupted
    if message['action'] == 'next' and presentating:
        if not interrupted and int(current_delay) > 0:
            interrupted = True
            emit('interrupt', broadcast=True)
        else:
            current_step += 1
            interrupted = False
            print("Current step: ", current_step)
            parameters = run_instructions(presentation_serial, current_step)
            if 'Screen' in parameters:
                try:
                    current_slide = int(parameters['Screen'])
                except ValueError:
                    current_slide = 1
            if 'Sound' in parameters:
                music_playing = parameters['Sound']
            if 'Delay' in parameters:
                current_delay = parameters['Delay']
            else:
                current_delay = 0
            if current_slide > total_slides or current_step > total_steps:
                current_slide = 1
                emit('redirect_home', broadcast=True)
            else:
                print("Delaying for: ", current_delay)
                print("Slide changed to: ", current_slide)
                emit('update_slide', {'slide': current_slide,
                                      'delay': current_delay}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
