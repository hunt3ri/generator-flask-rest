from flask import Blueprint

main = Blueprint('main', __name__, template_folder="templates")
swagger = Blueprint('swagger', __name__, static_folder='static/swagger-ui', url_prefix='/api-docs')

from . import controller
