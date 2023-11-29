from flask import Flask
from runner import *

app = Flask(__name__)


@app.route('/')
def home():

    classes = search_available_classes()
    return ", ".join(classes)


@app.route('/slides')
def next_slide():
    counter = 0


if __name__ == '__main__':
    app.run(debug=True)
