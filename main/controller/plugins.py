import os
import sys
from os import listdir


# This method returns an array with all filenames of plugins in path directory.
# Note: First position of that array, it will be the path of the plugins
def checkPlugins():
    print("check")
    validPlugins = []
    path = str(os.getcwd())+'/plugins/'
    validPlugins.append(path)

    try:
        for plugin in listdir(path):
            if plugin[len(plugin)-3:len(plugin)] == '.py' and plugin != '__init__.py':
                validPlugins.append(plugin)
        return validPlugins
    except:
        print("ERROR: there was a problem to read a plugin.\nCheck your plugins in app plugins directory.\n","Error: ", sys.exc_info()[0])
        return validPlugins
