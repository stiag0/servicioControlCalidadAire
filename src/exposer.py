from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
import json

from plugins import checkPlugins

exposer_app = Blueprint("exposer_app", __name__)

@exposer_app.route('/api/predictive_models/available', methods=['GET'])
def getAvailable():
    return jsonify(checkPlugins()[1:])