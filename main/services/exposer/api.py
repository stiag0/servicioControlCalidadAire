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
        sensor = body['sensor']
        fecha_i = body['fecha_hora_I']
        fecha_f = body['fecha_hora_F']
        fecha_pr = body['fecha_prediccion']
    except:
        return jsonify({'mensaje': 'Error: json malformado'})

    module = 'plugins.'+model
    try:
        mod = import_module(module)
        met = getattr(mod, 'start')
    except:
        return jsonify({'mensaje': 'Error: no se pudo importar el plugin'})

    prediction = met(sensor,fecha_i,fecha_f,fecha_pr)

    return jsonify({'prediccion': prediction})

