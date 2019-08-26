"""convenient function used to operate on posts"""

import random
import string
import os
import shutil


def generateID():
    """Generate a random post ID."""
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for _ in range(20))


def buildURL(dt, id):
    """Build post URL from datetime object and post ID."""
    return os.path.join(buildDateTimeURL(dt), id)


def buildDateTimeURL(dt):
    """Build string notation of post datetime."""
    return os.path.join(buildDateURL(dt), dt.strftime('%H/%M/%S'))


def buildDateURL(dt):
    """Build string of post date."""
    return dt.strftime('%Y/%m/%d')


def buildRawTimeStr(dt):
    """Build time string of datetime object without slashes."""
    return dt.strftime('%H%M%S')


def buildDatesFromFolders(directory):
    """Generate date hierachy of posts."""
    dates = []

    years = os.listdir(directory)
    for year in years:
        if year != '.gitignore':
            months = os.listdir(os.path.join(directory, year))
            for month in months:
                days = os.listdir(os.path.join(directory, year, month))
                for day in days:
                    dates.append(os.path.join(year, month, day))
    return dates


def makeString(integer):
    """Generate a normalized string from an int, int < 10 => prepend 0."""
    string = str(integer)
    if len(string) == 1:
        string = '0' + string

    return string


def getDisplayMode(string):
    """Return the display mode of a post."""
    return string.rpartition('-')[0].rpartition('-')[2]


def getTitle(string):
    """Return the title of a post."""
    return string.rpartition('-')[0].rpartition('-')[0].rpartition('-')[0].partition('-')[2]


def getTime(string):
    """Return the time a post was created."""
    return string.rpartition('-')[0].rpartition('-')[0].rpartition('-')[2]


def getID(string):
    """Return the ID of a post."""
    return string.partition('-')[0]


def getUser(string):
    """Return the user which has created the post."""
    user = string.rpartition('-')[2]
    if user == 'None':
        return None
    else:
        return user


def buildIrcChannelHash(channel_arr):
    """Create hash of channels, selected channel and the rest for view."""
    return {
        'selected': channel_arr[0],
        'channels': channel_arr
    }


def deleteDirTree(dir):
    """Delete a directory tree."""
    files = os.listdir(dir)
    if len(files) == 0:
        shutil.rmtree(dir)


def deleteRecursiveEmptyDirs(top_level_dir):
    """Delete empy directories."""
    deleteDirTree(top_level_dir)
    top_level_dir = top_level_dir.rpartition('/')[0]
    deleteDirTree(top_level_dir)
    top_level_dir = top_level_dir.rpartition('/')[0]
    deleteDirTree(top_level_dir)


def buildFileList(directory, year, month, day, id):
    """Build list of files corresponding to a post."""
    try:
        files = os.listdir(directory)
    except Exception:
        return []

    if len(files) == 0:
        return []
    files_arr = []
    for file in files:
        files_arr.append({
            'name': file,
            'link': '/'.join(['/getfile', str(year), makeString(month), makeString(day), id, file]),
            'dellink': '/'.join(['/delfile', str(year), makeString(month), makeString(day), id, file])
        })

    return files_arr


def sanitize_filename(s):
    """Remove illegal characters from filename."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    # I dont like spaces
    filename = filename.replace(' ', '_')

    return filename
