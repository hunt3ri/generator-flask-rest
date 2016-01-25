#!/usr/bin/env python

from flask.ext.script import Manager
from app import bootstrap_app

app = bootstrap_app()  # Initialise the flask app.
manager = Manager(app)

@manager.command
def test():
    """
    Helper function to enable us to simply run all tests from the command line, as follows:
    python manage.py test
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
