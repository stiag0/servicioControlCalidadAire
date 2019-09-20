from flask import Flask,Blueprint
from waitress import serve
from flask_cors import CORS
import sys
sys.path.insert(0, './')

from main.services.exposer.api import exposer_app

def expose():
    app = Flask(__name__)
    app.config.from_object(__name__)

    # It will allow external connections. Only for routes /api/*
    cors = CORS(app, resources= { r"/api/*": {"origins": "*"} } )

    # Puts instances of flask to serve only one
    app.register_blueprint(exposer_app)

    # Once the execution comes here, this thead won't be able execute animore instructions, only server requests.
    # It will run on a waitress server ready to deploy.
    serve(app, host='0.0.0.0', port=5000)