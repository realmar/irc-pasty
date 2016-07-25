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
        if not dirnames and dirpath != directory:
            day = dirpath.rpartition('/')[2]
            month = dirpath.rpartition('/')[0].rpartition('/')[2]
            year = dirpath.rpartition('/')[0].rpartition('/')[0].rpartition('/')[2]
            dates.append(os.path.join(year, month, day))

    if len(dates) == 1 and dates[0] == '':
        return []

    return dates

def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = '0' + string

    return string

def getDisplayMode(string):
    return string.rpartition('-')[2]

def getTitle(string):
    return string.rpartition('-')[0].rpartition('-')[0].partition('-')[2]

def getTime(string):
    return string.rpartition('-')[0].rpartition('-')[2]

def getID(string):
    return string.partition('-')[0]
