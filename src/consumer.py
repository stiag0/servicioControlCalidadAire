from flask import Flask,jsonify
import requests
from flask_cors import CORS
from datetime import datetime
import json
from pymongo import MongoClient
app = Flask(__name__)
CORS(app)
#MONGO_URL = 'mongodb://localhost'

# client = MongoClient(MONGO_URL)
# db =  client['sensorH']
# collection = db['sensores']

#posts = db.sensores
def consume():
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
    
    """print("Esto fue lo que se recuperó:\n")
    conta = 0
    for sensor in completo:
        print(str(conta), sensor['nombre'], " - ", sensor['ciudad'], " - ", sensor['barrio'])
        conta = conta + 1
    print("------------------------------------------------------------------------------------")
    """

    return completo
