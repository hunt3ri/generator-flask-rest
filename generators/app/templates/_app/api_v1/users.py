from flask import jsonify, request, current_app, url_for
from . import api


@api.route('/users/<int:id>')
def get_user(id):
    return jsonify(name="iain")
