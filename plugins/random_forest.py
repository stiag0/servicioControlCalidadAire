import numpy as np
#import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

from main.model.model import transformTD

def fit_model(tiempo, pm25):
    if(len(tiempo)<1):
        return -9999

    x = []
    for dato in tiempo:
        x.append([dato])
    x = np.array(x)
    y = np.array(pm25)

    regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
    regressor.fit(x, y)
    return regressor

def random_forest(regressor,prediccion):

    y_pred = regressor.predict([[prediccion]])

    #vizualizacion
    """
    print(y[len(y)-1])
    print(y_pred)
    print(type(y_pred))
    X_grid = np.arange(min(x), max(x), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(x, y, color = 'blue')
    # plot predicted data 

    labels = []
    for k in X_grid:
        print(str(transformTD(k)))
        labels.append(str(transformTD(k)))
    print("ya")

    pred = regressor.predict(X_grid)

    plt.plot(X_grid, pred,
            color = 'green')

    plt.xticks(X_grid, labels)

    plt.title('Random Forest Regression')
    plt.xlabel('Time')
    plt.ylabel('Pm 2.5')
    plt.show()
    """
    return y_pred[0]

def start(tiempo, pm25, fp):

    regresor = fit_model(tiempo, pm25)

    predictions = []
    for x in fp:
        predictions.append(random_forest(regresor,x))
    return predictions

    #return random_forest(tiempo, pm25, fp)
