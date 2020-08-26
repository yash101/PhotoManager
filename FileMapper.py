import os.path

def getCreationTimestamp(filename):
    try:
        return os.path.getctime(filename)
    except:
        return os.path.getmtime(filename)