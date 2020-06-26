import os
from constants import baseDirectory

def getFilePath(filename, dir = baseDirectory):
    print(dir, filename)
    return os.path.join(dir, filename)