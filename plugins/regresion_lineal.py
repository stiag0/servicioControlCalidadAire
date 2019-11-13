import numpy as np
#import matplotlib.pyplot as plt

from main.model.model import searchBetween,transformTS

def regresion_lineal(x,y,fecha_prediccion):

    n = len(x)
    if n == 0:
        return -9999
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
    """
    print("> Regresion lineal")
    print("R2=", R2)
    print("m=", m)
    print("b=", b)

    #Grafica los datos y su regresion
    plt.plot(x,y,'o', label='Datos')
    plt.plot(x, m*x+b, label='Ajuste')
    plt.xlabel('x')
    plt.xlabel('y')
    plt.title('Regresion lineal')
    plt.grid()
    plt.legend()
    plt.show()
    """
    return (m*fecha_prediccion)+b

def start(tiempo, pm25, fp):

    predictions = []
    for x in fp:
        predictions.append(regresion_lineal(tiempo,pm25,x))
    return predictions