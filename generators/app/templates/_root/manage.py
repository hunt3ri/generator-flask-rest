#!/usr/bin/env python

from flask.ext.script import Manager

from app import bootstrap_app

app = bootstrap_app()  # Initialise the flask app.
manager = Manager(app)



manager = Manager(app)

if __name__ == '__main__':
    manager.run()
