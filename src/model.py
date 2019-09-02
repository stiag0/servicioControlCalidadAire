from pymongo import MongoClient
import json

def connection(collection):
    MONGO_URL = 'mongodb://localhost'
    client = MongoClient(MONGO_URL)
    db = client['calidad_del_aire']
    collection = db[collection]
    return collection

# This method recives the collection(string) where we want to save it in and the dictionary to save.
def db_save(collection, document):
    try:
        # OJO aqui se debe hacer la validacion, insertar en el modelo solo las mediciones y ver si la estacion cambió
        db_connection = connection(collection)
        db_connection.insert_one(document)
        return True
    except:
        return False
