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

def filterGitignore(files):
    tmp = []
    for f in files:
        if f != '.gitignore':
            tmp.append(f)
    return tmp

def buildDatesFromFolders(directory):
    dates=[]

    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirnames:
            dates.append(dirpath.partition('/')[2])

    return dates

def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = '0' + string

    return string
