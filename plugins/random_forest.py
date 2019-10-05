import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

def random_forest(tiempo, pm25, prediccion):

    if(len(tiempo)<1):
        return -9999

    x = []
    for dato in tiempo:
        x.append([dato])
    x = np.array(x)
    y = np.array(pm25)

    regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
    regressor.fit(x, y)
    y_pred = regressor.predict([[prediccion]])
    return y_pred[0]

    #vizualizacion
    """
    print(y[len(y)-1])
    print(y_pred)
    print(type(y_pred))
    X_grid = np.arange(min(x), max(x), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(x, y, color = 'blue')
    # plot predicted data 
    plt.plot(X_grid, regressor.predict(X_grid),  
            color = 'green')  
    plt.title('Random Forest Regression') 
    plt.xlabel('Time') 
    plt.ylabel('Pm 2.5') 
    plt.show()
    """

def start(tiempo, pm25, fp):

    return random_forest(tiempo, pm25, fp)