import random, string, os, shutil

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

    years = os.listdir(directory)
    for year in years:
        if year != '.gitignore':
            months = os.listdir(os.path.join(directory, year))
            for month in months:
                days = os.listdir(os.path.join(directory, year, month))
                for day in days:
                    dates.append(os.path.join(year, month, day))
    '''
    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirnames and dirpath != directory:
            day = dirpath.rpartition('/')[2]
            month = dirpath.rpartition('/')[0].rpartition('/')[2]
            year = dirpath.rpartition('/')[0].rpartition('/')[0].rpartition('/')[2]
            dates.append(os.path.join(year, month, day))

    if len(dates) == 1 and dates[0] == '':
        return []
    '''

    print(dates)
    return dates

def makeString(integer):
    string = str(integer)
    if len(string) == 1:
        string = '0' + string

    return string

def getDisplayMode(string):
    return string.rpartition('-')[0].rpartition('-')[2]

def getTitle(string):
    return string.rpartition('-')[0].rpartition('-')[0].rpartition('-')[0].partition('-')[2]

def getTime(string):
    return string.rpartition('-')[0].rpartition('-')[0].rpartition('-')[2]

def getID(string):
    return string.partition('-')[0]

def getUser(string):
    user = string.rpartition('-')[2]
    if user == 'None':
        return None
    else:
        return user

def buildIrcChannelHash(channel_arr):
    return {
        'selected' : channel_arr[0],
        'channels' : channel_arr
    }

def delteDirTree(dir):
    files = os.listdir(dir)
    if len(files) == 0:
        shutil.rmtree(dir)

def deleteRecursiveEmptyDirs(top_level_dir):
    delteDirTree(top_level_dir)
    top_level_dir = top_level_dir.rpartition('/')[0]
    delteDirTree(top_level_dir)
    top_level_dir = top_level_dir.rpartition('/')[0]
    delteDirTree(top_level_dir)


def buildFileList(directory, year, month, day, id):
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        return []
    except:
        return True

    if len(files) == 0:
        return []
    files_arr = []
    for file in files:
        files_arr.append({
            'name' : file,
            'link' : '/'.join(['/getfile', str(year), makeString(month), makeString(day), id, file]),
            'dellink' : '/'.join(['/delfile', str(year), makeString(month), makeString(day), id, file])
        })

    return files_arr
