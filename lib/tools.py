import random, string
import datetime as dt

def generateID():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(20))

def generateDateTime():
    return {
        'date' : dt.datetime.today().strftime('%m-%d-%Y'),
        'time' : dt.datetime.today().strftime('%H:%M:%S')
    }
