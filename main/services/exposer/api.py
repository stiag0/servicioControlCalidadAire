from flask import jsonify
from flask import Blueprint
from flask import request
from importlib import import_module

from main.controller.plugins import checkPlugins

exposer_app = Blueprint("exposer_app", __name__)

@exposer_app.route('/api/predictive_models/available', methods=['GET'])
def getAvailable():
    return jsonify(checkPlugins()[1:])


@exposer_app.route('/api/predictive_models/run', methods=['POST'])
def runModel():

    body = request.json
    try:
        model = body['model']
    except:
        return jsonify({'mensaje': 'Error: json malformado'})

    module = 'plugins.'+model
    try:
        mod = import_module(module)
        met = getattr(mod, 'start')
    except:
        return jsonify({'mensaje': 'Error: no se pudo importar el plugin'})

    prediction = met([1],"2019-01-01T00:00:00","2019-01-02T00:00:00","2019-01-02T00:00:00")

    return jsonify({'prediccion': prediction})

