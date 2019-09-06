from flask import Flask
from flask import Blueprint
from waitress import serve
from flask_cors import CORS
import threading
import time

import sys
sys.path.insert(0, './')

from exposer import exposer_app
from consumer import consume
from model import connection,db_save

app = Flask(__name__)
app.config.from_object(__name__)

# It will allow external connections. Only for routes /api/*
cors = CORS(app, resources= { r"/api/*": {"origins": "*"} } )

# Puts instances of flask to serve only one
app.register_blueprint(exposer_app)

# This will be executed by a thread that consumes the api os SIATA, normalizes and saves the data.
def consumer():
    # It will take and save the data every 5 minutes.
    while True:
        # saveData(consume())
        #print (consume())
        sensores = consume()
        print("Se ejecuta la consulta, se estandariza y despues se guarda")

        """ example from new data structure
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
            {
            "fecha_hora": "2019-09-01T09:00:00",
            "PM2_5_CC_ICA": 62.53590252218173,
            "PM2_5_mean": 18.862121893925,
            "PM2_5_last": 19.3476636863,
            "temperatura": 22.185,
            "humedad_relativa": 68.9923333333
            }
        ]
        }
        """
        for i in sensores:
            a = db_save('mediciones',i)


        time.sleep(300)
# Once consumed the api, it will normalize and save the data
def saveData(data):
    pass



consumer_thread = threading.Thread(target=consumer)
consumer_thread.start()
# Once the execution comes here, this thead won't be able execute animore instructions, only server requests.
# It will run on a waitress server ready to deploy.
serve(app, host='0.0.0.0', port=5000)