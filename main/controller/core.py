import datetime
from importlib import import_module
from main.model.model import transformTS,searchBetween,transformTD,db_save_prediction

def predecir(metodo,dia_p):

    model = metodo
    dia = dia_p

    module = 'plugins.'+model
    predicciones = []
    #try:
    mod = import_module(module)
    met = getattr(mod, 'start')
    #except:
    #print('>Error: no se pudo importar el plugin')
    #return -1

    now = datetime.datetime.now()
    init_day = datetime.date.today() - datetime.timedelta(days=30)
    Fi = transformTS(init_day.strftime('%Y-%m-%dT%H:%M:%S'))

    fF = transformTS(now.strftime('%Y-%m-%dT%H:%M:%S'))
    #now = datetime.datetime.now()
    #predict_day = datetime.date.today() + datetime.timedelta(days=int(dia))
    predictions_hour = []

    for i in range(1,25):
        predictions_hour.append( now + datetime.timedelta(seconds=int( dia * ( i * 3600 ) )))
        predictions_hour[i-1] = float(transformTS(predictions_hour[i-1].strftime('%Y-%m-%dT%H:%M:%S')))

    #predict_hour = datetime.datetime.now() + datetime.timedelta(days=int(dia))

    #fp = transformTS(predict_day.strftime('%Y-%m-%dT%H:%M:%S'))

    predicciones = []
    search = searchBetween([],Fi,fF)

    for sensor in search:
        tiempo = []
        pm25 = []
        predictions_by_day = []

        for medicion in sensor['mediciones']:
            pm25.append(float(medicion['PM2_5_last']))
            tiempo.append(float(medicion['fecha_segundos']))

        del sensor['mediciones']
        sensor['codigo'] = sensor['_id']
        del sensor['_id']

        """
        for i in predictions_hour:
            predictions_by_day.append( met(tiempo,pm25,i) )
        """
        predictions_by_day = met(tiempo,pm25,predictions_hour)


        #for i in range(len(predictions_hour)):
        #predictions_hour[i] = transformTD(predictions_hour[i])

        data_predicction = []
        for i in range(len(predictions_by_day)):
            data_predicction.append({'fecha':str(transformTD(predictions_hour[i]))[5:-3],'PM2_5_last':predictions_by_day[i]})

        sensor['PM2_5_last'] = data_predicction
        sensor['PM2_5_mean'] = (sum(predictions_by_day)/24)

        predicciones.append(sensor)
        #predicciones.append({str(sensor['_id']):met(tiempo,pm25,fp)})

    collection = str(metodo)+"_"+str(dia_p)+"_dias"
    for x in predicciones:
        db_save_prediction(collection, x)