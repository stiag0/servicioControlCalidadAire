from flask import jsonify
from flask import Blueprint

from main.controller.plugins import checkPlugins

exposer_app = Blueprint("exposer_app", __name__)

@exposer_app.route('/api/predictive_models/available', methods=['GET'])
def getAvailable():
    return jsonify(checkPlugins()[1:])