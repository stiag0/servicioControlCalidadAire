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
        db_connection = connection(collection)
        
        #if db_connection.find({_codigo: document["codigo"]}) == {}:
        find_response = db_connection.find_one({'codigo': document["codigo"]})

        if find_response != None:
            """print(find_response['mediciones'][len(find_response['mediciones'])-1]["fecha_hora"],document["fecha_hora"])"""
            str1 = str(find_response['mediciones'][len(find_response['mediciones'])-1]["fecha_hora"]) 
            str2 = str(document["fecha_hora"])

            #a = datetime.datetime.strptime(str1, '%y-%m-%d %H:%M:%S').time()
            #b = datetime.datetime.strptime(str2, '%y-%m-%d %H:%M:%S').time()
            #print(a,b)
            #ideal a < b
            if  str1 != str2:
                medicion ={
                "fecha_hora": document["fecha_hora"],
                "PM2_5_CC_ICA":document["PM2_5_CC_ICA"],
                "PM2_5_mean":document["PM2_5_mean"],
                "PM2_5_last": document["PM2_5_last"],
                "temperatura": document["temperatura"],
                "humedad_relativa": document["humedad_relativa"]
                }
                try:
                    update_response = db_connection.update(
                        {"codigo": document["codigo"]},
                        {'$push': {'mediciones': medicion}}
                    )
                except:
                    return False

        else:
            print("> Se detectó un nuevo sensor!")
            print("> Id: ", document["nombre"])
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
            try:
                insert_response = db_connection.insert(newSensor)
            except:
                return False
            #print("fallo la insercion")

        #db_connection.insert_one(document)
        return True
    except:
        return False
