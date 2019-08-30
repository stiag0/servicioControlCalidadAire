from flask import Flask,jsonify
import requests
from flask_cors import CORS
from datetime import datetime
import pandas as pd
#biblioteca adicional a las de calse
#inicia flask
app =Flask(__name__)
#permite comunicacion entre puetos
CORS(app)

resp = requests.get('http://siata.gov.co:3000/cc_api/estaciones/listar/')
if resp.status_code != 200:
    # This means something went wrong.
    print('GET /tasks/ {}'.format(resp.status_code))
print(resp)
for todo_item in resp.json():
    if todo_item['online'] == "Y":
        print('{} {}'.format(todo_item['codigo'], todo_item['PM2_5_last']))

# url = 'http://siata.gov.co:3000/cc_api/estaciones/listar/'
# @app.route('/mostrar')
# def mostrar():
#     r = req.get(url)
#     data = pd.read_json(r.content)
#     return data

# app.run(port=5556,debug=True)