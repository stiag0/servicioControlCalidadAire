import requests
import json
from datetime import datetime
import time

from main.model.model import db_save

# This will be executed by a thread that consumes the api os SIATA, normalizes and saves the data.
def consume():

    # It will take and save the data every 5 minutes.
    while True:
        print("> Reques: 'http://siata.gov.co:3000/cc_api/estaciones/listar/' METHOD[GET]", datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))
        sensores = siata_request()

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
        saveData(sensores)
        time.sleep(300)

def siata_request():

    resp = requests.get('http://siata.gov.co:3000/cc_api/estaciones/listar/')
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /tasks/ {}'.format(resp.status_cod))
    
    print(resp)
    completo = []
 
    for todo_item in resp.json():
        if todo_item['online'] == "Y":
            if float(todo_item['PM2_5_last']) > 0.0:
                
                completo.append(todo_item)

    print("sensores online: ", len(completo),"\n")

    return completo

# Once consumed the api, it will normalize and save the data
def saveData(data):
    for sensor in data:
        save_response = db_save('mediciones', sensor)
        if save_response == False:
            print("Hubo un problema almacenando el dato: ")
            print(sensor,"\n")
    print("> Datos guardados satisfactoriamente")
    print("")