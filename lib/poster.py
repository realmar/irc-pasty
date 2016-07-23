import os
from datetime import datetime as dt

from lib.tools import *

def savePostTopLevel(title, content, datetime, id, directory):
    if datetime == None:
        datetime = dt.today()

    if id == None:
        id = generateID()
    if not savePost(title, content, datetime, id, directory):
        return buildURL(datetime, id)
    else:
        return True

def savePost(title, content, datetime, id, directory):
    try:
        directory = os.path.join(directory, buildDateURL(datetime))
        try: os.makedirs(directory)
        except: pass

        filename = os.path.join(directory, id + '-' + title + '-' + buildRawTimeStr(datetime))
        posts = os.listdir(directory)
        for post in posts:
            if id in post and not title in post:
                print('oha is here')
                print(directory)
                print(post)
                print(filename)
                os.rename(os.path.join(directory, post), filename)

        file = open(filename, 'w')
        file.write(content)
        file.close()
        return False
    except:
        print('write error')
        return True

def getPost(directory, datetime, id):
    try:
        directory = os.path.join(directory, buildDateURL(datetime))
        print(directory)
        posts = os.listdir(directory)
        title = None
        filename = None

        for post in posts:
            if id in post and buildRawTimeStr(datetime) in post:
                title = post.rpartition('-')[0].rpartition('-')[2]
                filename = post

        if title == None:
            return None
    except:
        print('list error')
        return None

    try:
        file = open(os.path.join(directory, filename), 'r')
        content = file.read()
        file.close()
        return { 'content' : content, 'title' : title, 'link' : buildURL(datetime, id) }
    except:
        print('read error')
        return False

def getAllPosts(directory='posts'):
    try:
        final_posts = []
        dates = buildDatesFromFolders(directory)
        dates.sort(key=lambda x: dt.strptime(x, '%Y/%m/%d'), reverse=True)
        print(dates)
        for date in dates:
            final_posts.append({
                'title' : None,
                'link' : None,
                'time' : date
            })
            posts = os.listdir(os.path.join(directory, date))
            posts.sort(key=lambda x: dt.strptime(x.rpartition('-')[2], '%H%M%S'), reverse=True)

            for post in posts:
                time = post.rpartition('-')[2]
                datetime = dt.strptime(date + time, '%Y/%m/%d%H%M%S')
                id = post.partition('-')[0]
                final_posts.append({
                    'title' : post.rpartition('-')[0].rpartition('-')[2],
                    'link' : buildURL(datetime, id),
                    'id' : id,
                    'time' : datetime.strftime('%H:%M:%S')
                })

        return final_posts
    except:
        print('exception in generate list of all')
        pass # do exception handling
