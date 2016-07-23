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
        file = open(os.path.join(directory, id + '-' + title + '-' + buildRawTimeStr(datetime)), 'w')
        file.write(content)
        file.close()
        return False
    except:
        print('write error')
        return True

def getPost(directory, date, time, id):
    try:
        directory = os.path.join(directory, date)
        posts = os.listdir(directory)
        title = None

        for post in posts:
            if id in post and time in post:
                title = post.rpartition('-')[0].rpartition('-')[2]

        if title == None:
            return None

        file = open(os.path.join(directory, id + '-' + title + '-' + time), 'r')
        content = file.read()
        file.close()
        return { 'content' : content, 'title' : title, 'link' : os.path.join(date, time, id) }
    except:
        return False

def getAllPosts():
    try:
        final_posts = []

        dates_tmp = os.listdir('posts')
        dates = []

        for date in dates_tmp:
            if date != '.gitignore':
                dates.append(date)

        dates.sort(key=lambda x: dt.datetime.strptime(x, '%m-%d-%Y'), reverse=True)

        for date in dates:
            final_posts.append({
                'title' : None,
                'link' : None,
                'time' : date
            })
            print(date)
            posts = os.listdir(os.path.join('posts', date))
            posts.sort(key=lambda x: dt.datetime.strptime(x.rpartition('-')[2], '%H:%M:%S'), reverse=True)

            for post in posts:
                time = post.rpartition('-')[2]
                hasht = post.partition('-')[0]
                final_posts.append({
                    'title' : post.rpartition('-')[0].rpartition('-')[2],
                    'link' : os.path.join(date, time, hasht),
                    'hash' : hasht,
                    'time' : time
                })

        return final_posts
    except:
        print('exception in generate list of all')
        # pass # do exception handling
