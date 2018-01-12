"""
    Server module defines the web server
"""
import os
from flask import Flask, render_template

static_dir = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
    'client',
    'dist'
)

template_dir = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
    'client'
)

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route('/')
def show_home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
