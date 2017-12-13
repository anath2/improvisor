"""
    Server module defines the web server
"""
import os
from flask import Flask, render_template

template_dir = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
    'static'
)
app = Flask(__name__, template_folder=template_dir)
@app.route('/')
def show_home():
    """
        Homepage
    """

    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_input():
    """
        Post sound data
    """
    pass
    # Process the sound data
