from main.controller.core import predecir
from main.controller.plugins import checkPlugins

models = []
for x in checkPlugins()[1:]:
    models.append(x[:-3])
print(models)
for i in models:
    for j in range(7):
    predecir(models[i],j+1)
