import os
from datetime import datetime as dt

from lib.tools import *

def savePostTopLevel(title, content, display_mode, datetime, id, directory, remote_user=None):
    if datetime == None:
        datetime = dt.today()

    if id == None:
        id = generateID()
    if not savePost(title, content, display_mode, datetime, id, directory, remote_user):
        return buildURL(datetime, id)
    else:
        return True

def savePost(title, content, display_mode, datetime, id, directory, remote_user=None):
    try:
        directory = os.path.join(directory, buildDateURL(datetime))
        try: os.makedirs(directory)
        except: pass
        remote_user = str(remote_user)
        filename = os.path.join(directory, id + '-' + title + '-' + buildRawTimeStr(datetime) + '-' + str(display_mode) + '-' + remote_user)
        posts = os.listdir(directory)
        for post in posts:
            if id in post and not title in post:
                os.rename(os.path.join(directory, post), filename)
            if id in post and title in post and getDisplayMode(post) != display_mode:
                os.rename(os.path.join(directory, post), filename)

        file = open(filename, 'w')
        file.write(content)
        file.close()
        return False
    except Exception as e:
        print('savePost ' + str(e))
        return True

def getPost(directory, datetime, id):
    try:
        directory = os.path.join(directory, buildDateURL(datetime))
        posts = os.listdir(directory)
        title = None
        display_mode = None
        filename = None

        for post in posts:
            if id in post and buildRawTimeStr(datetime) in post:
                title = getTitle(post)
                display_mode = getDisplayMode(post)
                filename = post
                user = getUser(post)

        if title == None or display_mode == None:
            return None
    except Exception as e:
        print('getPost listdir' + str(e))
        return True

    if user == 'None':
        user = None

    try:
        file = open(os.path.join(directory, filename), 'r')
        content = file.read()
        file.close()
        return {
            'content' : content,
            'title' : title,
            'link' : buildURL(datetime, id),
            'display_mode' : display_mode,
            'user' : user
        }
    except Exception as e:
        print('getPost write ' + str(e))
        return True

def getAllPosts(directory):
    try:
        final_posts = []
        dates = buildDatesFromFolders(directory)
        if len(dates) == 0:
            return []

        dates.sort(key=lambda x: dt.strptime(x, '%Y/%m/%d'), reverse=True)
        for date in dates:
            posts = os.listdir(os.path.join(directory, date))
            posts.sort(key=lambda x: dt.strptime(getTime(x), '%H%M%S'), reverse=True)

            if len(posts) == 0:
                continue

            final_posts.append({
            'title' : None,
            'link' : None,
            'time' : date
            })


            for post in posts:
                time = getTime(post)
                datetime = dt.strptime(date + time, '%Y/%m/%d%H%M%S')
                id = getID(post)
                final_posts.append({
                    'title' : getTitle(post),
                    'link' : buildURL(datetime, id),
                    'time' : datetime.strftime('%H:%M:%S'),
                    'user' : getUser(post)
                })

        return final_posts
    except Exception as e:
        print('getAllPosts listdir ' + str(e))
        return True
