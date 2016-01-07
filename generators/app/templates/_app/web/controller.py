from flask import render_template
from . import main


# Controller to launch the Welcome Page, for Rest APIs you shouldn't be extending this very much
@main.route('/')
def index():
    return render_template('index.html')
