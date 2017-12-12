"""
    Server module defines the web server
"""
import os
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_home():
    """
        Homepage
    """
    return render_template('improvisor_page')

@app.route('/', methods=['POST'])
def get_input():
    """
        Post sound data
    """
    pass
    # Process the sound data
