from flask import jsonify
from flask import Blueprint
from flask import request
from flask import render_template, Response, redirect, url_for
from importlib import import_module
from main.model.model import transformTS,searchBetween,searchAll
from main.controller.plugins import checkPlugins
import datetime

exposer_app = Blueprint("exposer_app", __name__)

@exposer_app.route('/api/predictive_models/available', methods=['GET'])
def getAvailable():
    models = []
    for x in checkPlugins()[1:]:
        models.append(x[:-3])
    return jsonify(models)

@exposer_app.route('/api/predictive_models/run', methods=['POST'])
def runModel():

    body = request.json
    try:
        model = body['model']
        dia = body['dia']
    except:
        return jsonify({'mensaje': 'Error: json malformado'})

    data = []
    data = searchAll(str(model)+"_"+str(dia)+"_dias")

    return jsonify(data)

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

@exposer_app.route("/adminCenter",methods=['GET'])
def allTable():
    return render_template('admin.html')

@exposer_app.route("/api/graficado",methods=['POST'])
def ShowAll():
    body = request.get_json()
    print(body)
    fecha1 = transformTS(body['fechaI'])
    fecha2 = transformTS(body['fechaF'])
    sensores = body['sensores']
    if len(sensores) > 0:
        sensores = sensores.split(',')
    else:
        sensores = []
    for x in range(len(sensores)):
        sensores[x] = int (sensores[x]) 
    #print (fecha1,fecha2,sensores)
    datos = searchBetween(sensores,fecha1,fecha2,False)
    #print (datos)
    return jsonify(datos)