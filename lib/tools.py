import random, string, os

def generateID():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(20))

def buildURL(dt, id):
    return os.path.join(buildDateTimeURL(dt), id)

def buildDateTimeURL(dt):
    return os.path.join(buildDateURL(dt), dt.strftime('%H/%M/%S'))

def buildDateURL(dt):
    return dt.strftime('%Y/%m/%d')

def buildRawTimeStr(dt):
    return dt.strftime('%H%M%S')
