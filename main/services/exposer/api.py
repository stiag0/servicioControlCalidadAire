from flask import jsonify
from flask import Blueprint
from flask import request
from importlib import import_module
from main.model.model import transformTS,searchBetween
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
        sensores = body['sensores']
        fecha_i = body['fecha_hora_I']
        fecha_f = body['fecha_hora_F']
        fecha_pr = body['fecha_prediccion']
    except:
        return jsonify({'mensaje': 'Error: json malformado'})

    module = 'plugins.'+model
    
    #try:
    mod = import_module(module)
    met = getattr(mod, 'start')
    #except:
    #return jsonify({'mensaje': 'Error: no se pudo importar el plugin'})

    Fi = transformTS(fecha_i) 
    fF = transformTS(fecha_f)
    fp = transformTS(fecha_pr)

    predicciones = []
    search = searchBetween(sensores,Fi,fF)
    print("sensores:",sensores)

    for sensor in search:

        tiempo = []
        pm25 = []

        for medicion in sensor['mediciones']:
            pm25.append(float(medicion['PM2_5_last']))
            tiempo.append(medicion['fecha_segundos'])

        """
        cont = 0
        for x in range(len(tiempo)):
            if tiempo[x] > Fi and tiempo[x] < fF:
                cont += 1
        """

        predicciones.append({str(sensor['_id']):met(tiempo,pm25,fp)})

    return jsonify(predicciones)

@exposer_app.route('/api/model/search_between', methods=['POST'])
def getHB():
    body = request.json
    try:
        fecha1 = transformTS(body['fechaI'])
        fecha2 = transformTS(body['fechaF'])
        sensores = body['sensores']
    except:
        return jsonify({'mensaje': 'Error: no se pudo importar el plugin'})
    return jsonify(searchBetween(sensores,fecha1,fecha2,False))