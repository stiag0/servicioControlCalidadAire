from pymongo import MongoClient
import json
import datetime

def connection(collection):
    MONGO_URL = 'mongodb://localhost'
    client = MongoClient(MONGO_URL)
    db = client['calidad_del_aire']
    collection = db[collection]
    return collection
def transformTS (sdateFormat):
    a = int(sdateFormat[:4])
    m = int(sdateFormat[5:7])
    d = int(sdateFormat[8:10])
    h = int(sdateFormat[11:13])
    mi = int(sdateFormat[14:16])
    s = int(sdateFormat[17:19])
    fS = (a*31536000)+(m*2592000)+(d*86400)+(h*3600)+(mi*60)+(s)
    return fS
def transformTD(secondsDate):
    ano = secondsDate/31536000
    mes = secondsDate%31536000
    dia = mes%2592000
    mes = mes/2592000
    hora = dia%86400
    dia = dia/86400
    minuto = hora%3600
    hora = hora/3600
    segundo = minuto%60
    minuto = minuto/60

    if int(dia) == 0:
        return datetime.datetime(int(ano),int(mes),int(dia+1),int(hora),int(minuto),int(segundo))
    return datetime.datetime(int(ano),int(mes),int(dia),int(hora),int(minuto),int(segundo))

def searchOL(lista,fs):
    if len(lista) == 0:
        return 0
    i = len(lista)-1
    for medicion in reversed(lista):
        if medicion["fecha_segundos"]==fs:
            #print("falsa alarma")
            return False
        if medicion["fecha_segundos"]<fs:
            #print(i,"es menor")
            return i+1
        else:
            i = i-1
    return 0
            
# This method recives the collection(s
# tring) where we want to save it in and the dictionary to save.
def db_save(collection, document):
    db_connection = connection(collection)
    #if db_connection.find({_codigo: document["codigo"]}) == {}:
    find_response = db_connection.find_one({'_id': document["codigo"]})

    str2 = transformTS(document["fecha_hora"]) 
    medicion ={
            "fecha_segundos": str2,
            "PM2_5_CC_ICA":document["PM2_5_CC_ICA"],
            "PM2_5_mean":document["PM2_5_mean"],
            "PM2_5_last": document["PM2_5_last"],
            "temperatura": document["temperatura"],
            "humedad_relativa": document["humedad_relativa"]
            }

    if find_response != None:
        """print(find_response['mediciones'][len(find_response['mediciones'])-1]["fecha_hora"],document["fecha_hora"])"""
        #str1 = find_response['mediciones'][len(find_response['mediciones'])-1]["fecha_segundos"] 

        a = searchOL(find_response['mediciones'], str2)
        
        if  a == len(find_response['mediciones']):
            #print("si")
            try:
                update_response = db_connection.update(
                    {"_id": document["codigo"]},
                    {'$push': {'mediciones': medicion}}
                )

            except:
                print("> Error: No se pudo actualizar 1")
                return False
        else:
            if a == False:
                return True

            if a < len(find_response['mediciones']):
                #print("si interno")
                try:
                    update_response = db_connection.update(
                        {"_id": document["codigo"]},
                        {'$push': {"mediciones": {
                                    "$each": [medicion],
                                    "$position": a
                                    }
                                }
                        }
                    )
                    
                except:
                    print("> Error: No se pudo actualizar 2")
                    return False
    else:
        #print("> Msg: Se detectó un nuevo sensor!")
        #print("- Id: ", document["nombre"])

        #fS = transformTS(document["fecha_hora"])
        newSensor = {
        "altitud": document["altitud"],
        "barrio": document["barrio"],
        "vereda": document["vereda"],
        "ciudad": document["ciudad"],
        "nombre": document["nombre"],
        "_id": document["codigo"],
        "latitude": document["latitude"],
        "longitude": document["longitude"],
        "mediciones":[medicion]
        }

        #print(json.dumps(newSensor))
        try:
            insert_response = db_connection.insert(newSensor)
        except:
            return False
        #print("fallo la insercion")

    #db_connection.insert_one(document)
    return True


def db_save_prediction(collection, document):
    db_connection = connection(collection)

    try:
        find_response = db_connection.find_one({"codigo": document["codigo"]})
    except:
        print("> Error: No se pudo conectar a la base de datos")
        return False

    if find_response != None:
        try:
            update_response = db_connection.update({"codigo": document["codigo"]}, document)
        except:
            print("> Error: No se pudo actualizar la prediccion con codigo: ", document["codigo"])
            return False
        
        return True
    else:
        #------------aqui voy-----------------
        try:
            insert_response = db_connection.insert(document)
        except:
            print("> Error: No se pudo insertar la prediccion con codigo: ", document["codigo"])
            return False
        
        return True

def searchAll(collection):
    db_connection = connection(collection)
    data = []
    try:
        find_response = db_connection.find()
    except:
        print("> Error: No se pudo conectar a la base de datos")
        return []
    if find_response != None:
        for x in find_response:
            del x['_id']
            data.append(x)
        return data
    return []



def searchBetween(sensores,date1,date2,en_seg = True):
    lista = []
    try:
        db_connection = connection("mediciones")
        #if db_connection.find({_codigo: document["codigo"]}) == {}:
        if len(sensores)<1:
            find_response = db_connection.find()
            if find_response != None:
                for sensor in find_response:
                    newSensor = {
                    "altitud": sensor["altitud"],
                    "barrio": sensor["barrio"],
                    "vereda": sensor["vereda"],
                    "ciudad": sensor["ciudad"],
                    "nombre": sensor["nombre"],
                    "_id": sensor["_id"],
                    "latitude": sensor["latitude"],
                    "longitude": sensor["longitude"],
                    "mediciones":[]
                    }
                    for medicion in sensor["mediciones"]:
                        if en_seg:
                            if medicion["fecha_segundos"] < date2 and medicion["fecha_segundos"] > date1:
                                newSensor["mediciones"].append(medicion)
                            if medicion["fecha_segundos"] > date2 and medicion["fecha_segundos"] > date1:
                                break
                        else:
                            copiaSeg = medicion["fecha_segundos"]
                            if copiaSeg < date2 and copiaSeg > date1:
                                #fecha = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
                                medicion["fecha_segundos"] = transformTD(medicion["fecha_segundos"]).strftime('%Y-%m-%dT%H:%M:%S')
                                newSensor["mediciones"].append(medicion)
                            if copiaSeg > date2 and copiaSeg > date1:
                                break

                    if len(newSensor["mediciones"])>0:
                        lista.append(newSensor)
        else:
            for codigo in sensores:
                find_response = db_connection.find_one({'_id': codigo})
                if find_response != None:
                    newSensor = {
                    "altitud": find_response["altitud"],
                    "barrio": find_response["barrio"],
                    "vereda": find_response["vereda"],
                    "ciudad": find_response["ciudad"],
                    "nombre": find_response["nombre"],
                    "_id": find_response["_id"],
                    "latitude": find_response["latitude"],
                    "longitude": find_response["longitude"],
                    "mediciones":[]
                    }
                    for medicion in find_response["mediciones"]:
                        if en_seg:
                            if medicion["fecha_segundos"] < date2 and medicion["fecha_segundos"] > date1:
                                newSensor["mediciones"].append(medicion)
                            if medicion["fecha_segundos"] > date2 and medicion["fecha_segundos"] > date1:
                                break
                        else:
                            copiaSeg = medicion["fecha_segundos"]
                            if copiaSeg < date2 and copiaSeg > date1:
                                
                                medicion["fecha_segundos"] = transformTD(medicion["fecha_segundos"]).strftime('%Y-%m-%dT%H:%M:%S')
                                newSensor["mediciones"].append(medicion)

                            if copiaSeg > date2 and copiaSeg > date1:
                                break
                    lista.append(newSensor)
        return lista
    except:
        return []