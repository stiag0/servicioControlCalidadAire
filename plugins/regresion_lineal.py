import numpy as np
import matplotlib.pyplot as plt

from main.model.model import searchBetween,transformTS

def regresion_lineal(x,y,fecha_prediccion):
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x*x)
    sumy2 = sum(y*y)
    sumxy = sum(x*y)
    promx = sumx/n
    promy = sumy/n

    m = (sumx*sumy - n*sumxy) / (sumx**2 - n*sumx2)
    b = promy - m*promx

    sigmax = np.sqrt(sumx2/n - promx**2)
    sigmay = np.sqrt(sumy2/n - promy**2)
    sigmaxy = sumxy/n - promx*promy

    R2 = (sigmaxy/(sigmax*sigmay))**2
    print("R2=", R2)
    print("m=", m)
    print("b=", b)

    plt.plot(x,y,'o', label='Datos')
    plt.plot(x, m*x+b, label='Ajuste')
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Regresion lineal')
    plt.grid()
    plt.legend()
    plt.show()

    return m*fecha_prediccion+b

def start(sensores, fecha_hora_I, fecha_hora_F, fecha_prediccion):

    Fi = transformTS(fecha_hora_I) 
    fF = transformTS(fecha_hora_F)
    fp = transformTS(fecha_prediccion)
    print("Inicial:",Fi)
    print("Final:",fF)
    print("Fecha prediccion:",fp)

    fp = 63673914540
    tiempo = []
    pm25 = []

    for sensor in searchBetween(sensores,Fi,fF):
        for medicion in sensor['mediciones']:
            pm25.append(float(medicion['PM2_5_last']))
            tiempo.append(medicion['fecha_segundos'])

    print(len(tiempo))
    print(len(pm25))
    print(tiempo)
    print(pm25)
    cont = 0
    for x in range(len(tiempo)):
        if tiempo[x] > Fi and tiempo[x] < fF:
            cont += 1

    # Al graficar los datos se observa una tendencia lineal
    #datos.plot.scatter(x='tiempo', y='pm2.5')

    return regresion_lineal(tiempo,pm25,fp)
