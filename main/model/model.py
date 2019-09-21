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
            str1 = find_response['mediciones'][len(find_response['mediciones'])-1]["fecha_segundos"] 
            str2 = document["fecha_hora"]

            a = int(str2[:4])
            m = int(str2[5:7])
            d = int(str2[8:10])
            h = int(str2[11:13])
            mi = int(str2[14:16])
            s = int(str2[17:19])
            fS = (a*31536000)+(m*2592000)+(d*86400)+(h*3600)+(mi*60)+(s)
            #ideal a < b
            print(str1,"<",fS)
            if  str1 < fS:
                print("si")
                medicion ={
                "fecha_segundos": fS,
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
                    print("NO pudo actualizar")
                    return False
            else:
                print("NO")
        else:
            print("> Se detectó un nuevo sensor!")
            print("> Id: ", document["nombre"])
            a = int(document["fecha_hora"][:4])
            m = int(document["fecha_hora"][5:7])
            d = int(document["fecha_hora"][8:10])
            h = int(document["fecha_hora"][11:13])
            mi = int(document["fecha_hora"][14:16])
            s = int(document["fecha_hora"][17:19])
            fS = (a*31536000)+(m*2592000)+(d*86400)+(h*3600)+(mi*60)+(s)
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
                "fecha_segundos": fS,
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
