import pandas as pd
import numpy as np
#import matplotlib.pylab as plt
from main.model.model import transformTD
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

"""
#from pandas.plotting import register_matplotlib_converters
def test_stationarity(timeseries):
    
    #Determing rolling statistics
    #rolmean = pd.rolling_mean(timeseries, window=12)
    rolmean = pd.Series(timeseries).rolling(window=12).mean()
    #rolstd = pd.rolling_std(timeseries, window=12)#Plot rolling statistics:
    rolstd = pd.Series(timeseries).rolling(window=12).std()
    plt.plot(timeseries, color='blue',label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
"""

def ARIMA_MODEL(X,Y,X_predict):

    x1 = []
    for x in range(len(X)):
        x1.append(str(transformTD(X[x])))
    """
    data = []
    for x in range(len(X)):
        data.append([str(transformTD(X[x])),Y[x]])
    #data = np.array(data)
    """
    data = pd.DataFrame({'5_min': x1, 'pm25': Y})

    con = data['5_min']
    data['5_min'] = pd.to_datetime(data['5_min'])
    data.set_index('5_min', inplace = True)

    ts = data['pm25']
    
    #test_stationarity(ts)
    #exit(0)
    #test_stationarity(ts)
    #plt.plot(ts)
    #plt.show()

    ts_log = np.log(ts)
    #plt.plot(ts_log)
    #plt.show()
    moving_avg = pd.Series(ts_log).rolling(window=288).mean() # NOTA: para despliegue con bastantes datos, window será de 288, para que sean series diarias
    #plt.plot(ts_log)
    #plt.plot(moving_avg, color='red')
    #plt.show()

    ts_log_diff = ts_log - ts_log.shift()
    ts_log_moving_avg_diff = ts_log - moving_avg
    ts_log_moving_avg_diff.dropna(inplace=True)
    #print(ts_log_moving_avg_diff.head())
    #test_stationarity(ts_log_moving_avg_diff)

    try:
        model = ARIMA(ts_log, order=(2,1,2))
        results_ARIMA = model.fit(disp=-1)
    except:
        try:
            model = ARIMA(ts_log, order=(2,1,1))
            results_ARIMA = model.fit(disp=-1)
        except:
            try:
                model = ARIMA(ts_log, order=(2,1,0))
                results_ARIMA = model.fit(disp=-1)
            except:
                return []
    #plt.plot(ts_log_diff)
    #plt.plot(results_ARIMA.fittedvalues, color='red')
    #plt.title('%RSA: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
    #plt.show()

    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy= True)
    #print(predictions_ARIMA_diff.head())

    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    #print(predictions_ARIMA_diff_cumsum.head())

    predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value = 0)
    #print(predictions_ARIMA_log.head())

    """
    print(ts)
    start_index = transformTD(X[len(X)-1] + 300)
    end_index = transformTD(X[len(X)-1] + 1500)
    print(start_index)
    print(end_index)
    print(type(start_index))
    print(type(end_index))"""

    #print(ts.index)
    #forecast = results_ARIMA.predict(224,228)
    
    ultima = X[len(X)-1]
    primera = X_predict[len(X_predict)-1]
    diferencia = int((primera-ultima)/300) #diferencia entre el ultimo valor de entranamiento y la primer prediccion que queremos

    forecast = results_ARIMA.forecast(steps=(diferencia+288))[0]

    print("ultima data", Y[len(Y)-10:len(Y)])
    print("print del forecast",forecast)
    print()
    forecast = forecast[diferencia:]
    predicciones = []

    for i in range(24):
        predicciones.append((sum(forecast[0:12])/12))
        forecast = forecast[12:]
    return predicciones

    """
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    plt.plot(ts)
    plt.plot(predictions_ARIMA, color='red')
    plt.show()
    """

def start(tiempo, pm25, fp):

    return ARIMA_MODEL(tiempo,pm25,fp)
