import datetime
from importlib import import_module
from main.model.model import transformTS,searchBetween,transformTD,db_save_prediction

def predecir(metodo,dia_p):
    
    model = metodo
    dia = dia_p

    module = 'plugins.'+model

    predicciones = []
    try:
        mod = import_module(module)
        met = getattr(mod, 'start')
    except:
        print('>Error: no se pudo importar el plugin')
        return -1

    today = datetime.date.today()
    predict_day = datetime.date.today() + datetime.timedelta(days=int(dia))
    init_day = datetime.date.today() - datetime.timedelta(days=30)

    fF = transformTS(today.strftime('%Y-%m-%dT%H:%M:%S'))
    Fi = transformTS(init_day.strftime('%Y-%m-%dT%H:%M:%S'))
    fp = transformTS(predict_day.strftime('%Y-%m-%dT%H:%M:%S'))

    predicciones = []
    search = searchBetween([],Fi,fF)

    for sensor in search:

        tiempo = []
        pm25 = []

        for medicion in sensor['mediciones']:
            pm25.append(float(medicion['PM2_5_last']))
            tiempo.append(medicion['fecha_segundos'])

        del sensor['mediciones']
        sensor['codigo'] = sensor['_id']
        del sensor['_id']
        sensor['PM2_5_last'] = met(tiempo,pm25,fp)

        predicciones.append(sensor)
        #predicciones.append({str(sensor['_id']):met(tiempo,pm25,fp)})

    collection = str(metodo)+"_"+str(dia_p)+"_dias"
    for x in predicciones:
        db_save_prediction(collection, x)
