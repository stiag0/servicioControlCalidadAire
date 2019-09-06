from pymongo import MongoClient
import json
import datetime

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
        
        print(document["codigo"],document['barrio'])
        #if db_connection.find({_codigo: document["codigo"]}) == {}:
        k = db_connection.find_one({'codigo': document["codigo"]})
        print(k)
        if k != None:
            print(k['mediciones'][len(k['mediciones'])-1]["fecha_hora"],document["fecha_hora"])
            str1 = str(k['mediciones'][len(k['mediciones'])-1]["fecha_hora"]) 
            str2 = str(document["fecha_hora"])
            #print(str1,str2)
            #a = datetime.datetime.strptime(str1, '%y-%m-%d %H:%M:%S').time()
            #b = datetime.datetime.strptime(str2, '%y-%m-%d %H:%M:%S').time()
            #print(a,b)
            #ideal a < b
            if  str1 != str2: 
                print("es mas viejo")
                medicion ={
                "fecha_hora": document["fecha_hora"],
                "PM2_5_CC_ICA":document["PM2_5_CC_ICA"],
                "PM2_5_mean":document["PM2_5_mean"],
                "PM2_5_last": document["PM2_5_last"],
                "temperatura": document["temperatura"],
                "humedad_relativa": document["humedad_relativa"]
                }
                db_connection.update(
                    {"codigo": document["codigo"]},
                    {'$push': {'mediciones': medicion}}
                )
        else:
            print("nuevo sensor")
            newSensor = {
            "altitud": document["altitud"],
            "barrio": document["barrio"],
            "vereda": document["vereda"],
            "ciudad": document["ciudad"],
            "nombre": document["nombre"],
            "codigo": document["codigo"],
            "latitude": document["latitude"],
            "longitude": document["longitude"],
            "mediciones":[
                {
                "fecha_hora": document["fecha_hora"],
                "PM2_5_CC_ICA":document["PM2_5_CC_ICA"],
                "PM2_5_mean":document["PM2_5_mean"],
                "PM2_5_last": document["PM2_5_last"],
                "temperatura": document["temperatura"],
                "humedad_relativa": document["humedad_relativa"]
                }
            ]
            }

            #print(json.dumps(newSensor))
            db_connection.insert(newSensor)
                

        #db_connection.insert_one(document)
        return True
    except:
        return False
