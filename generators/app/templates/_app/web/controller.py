from flask import render_template, current_app
from . import main, swagger


@main.route('/')
def index():
    """
    Controller to launch the Welcome Page.  For RESTful APIs you shouldn't need to extend this very much.
    :return: The Welcome Page
    """
    api_url = current_app.config['API_DOCS_URL']
    return render_template('welcome.html', doc_link=api_url)


@swagger.route('/', defaults={'path': 'index.html'})
@swagger.route('/<path:path>')
def swagger_ui(path):
    """
    Here we're serving the static Swagger-UI files, added a catch-all route as there is a whole bunch of associated
    static files.  Swagger-UI github repo is here https://github.com/swagger-api/swagger-ui
    :param path: The path to the requested file
    :return: The requested file.
    """
    return swagger.send_static_file(path)
