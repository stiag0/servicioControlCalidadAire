from flask import Flask,jsonify
import requests
from flask_cors import CORS
from datetime import datetime
import json
from pymongo import MongoClient
#import pandas as pd
#biblioteca adicional a las de calse
#inicia flask
app = Flask(__name__)
#permite comunicacion entre puertos
CORS(app)
MONGO_URL = 'mongodb://localhost'

client = MongoClient(MONGO_URL)
db =  client['sensorH']
collection = db['sensores']

posts = db.sensores
def consume():
    resp = requests.get('http://siata.gov.co:3000/cc_api/estaciones/listar/')
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /tasks/ {}'.format(resp.status_code))
    print(resp)
    completo = []
    dato_sensor = {
        "altitud": 1549,
        "barrio": "San Germán",
        "vereda": "Zona Urbana",
        "ciudad": "Medellin",
        "estado": "A",
        "nombre": "4",
        "codigo": 4,
        "latitude": 6.2704115,
        "longitude": -75.58704490000002,
        "mediciones":[
            
        ]
    }
    medicion = {
            "fecha_hora": "2019-09-01T09:00:00",
            "PM2_5_CC_ICA": 62.53590252218173,
            "PM2_5_mean": 18.862121893925,
            "PM2_5_last": 19.3476636863,
            "temperatura": 22.185,
            "humedad_relativa": 68.9923333333
            }
    funcionales = 0 
    for todo_item in resp.json():
        if todo_item['online'] == "Y":
            if float(todo_item['PM2_5_last']) > 0.0:
                funcionales = funcionales+1
                
                dato_sensor['altitud'] = todo_item['altitud']
                dato_sensor['barrio'] = todo_item['barrio']
                dato_sensor['vereda'] = todo_item['vereda']
                dato_sensor['ciudad'] = todo_item['ciudad']
                dato_sensor['estado'] = todo_item['estado']
                dato_sensor['nombre'] = todo_item['nombre']
                dato_sensor['codigo'] = todo_item['codigo']
                dato_sensor['latitude'] = todo_item['latitude']
                dato_sensor['longitude'] = todo_item['longitude']

                medicion['fecha_hora'] = todo_item['fecha_hora']
                medicion['PM2_5_CC_ICA'] = todo_item['PM2_5_CC_ICA']
                medicion['PM2_5_mean'] = todo_item['PM2_5_mean']
                medicion['PM2_5_last'] = todo_item['PM2_5_last']
                medicion['temperatura'] = todo_item['temperatura']
                medicion['humedad_relativa'] = todo_item['humedad_relativa']
                if len(dato_sensor['mediciones']) < 1:
                    dato_sensor['mediciones'].append(medicion)
                    
                completo.append(dato_sensor)
                #print(dato_sensor)
                #post_id = posts.insert_one(dato_sensor)
                #print('{} {}'.format(todo_item['codigo'], todo_item['PM2_5_last']))
    #print(completo)
    print("sensores usables ",funcionales)
    return completo

    # url = 'http://siata.gov.co:3000/cc_api/estaciones/listar/'
    # @app.route('/mostrar')
    # def mostrar():
    #     r = req.get(url)
    #     data = pd.read_json(r.content)
    #     return data

    # app.run(port=5556,debug=True)
