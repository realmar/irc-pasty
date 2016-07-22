import os

def savePost(directory, id, content, title):
    try:
        file = open(os.path.join(directory, id + '-' + title), 'w')
        file.write(content)
        file.close()
        return False
    except:
        print('write error')
        return True

def getPost(id):
    try:
        posts = os.listdir('posts')
        title = None

        for post in posts:
            if id in post:
                title = post.rpartition('-')[2]

        if title == None:
            return None

        file = open(os.path.join('posts', id + '-' + title), 'r')
        content = file.read()
        file.close()
        return { 'content' : content, 'title' : title }
    except:
        return False

def getAllPosts():
    try:
        posts = os.listdir('posts')
        final_posts = []

        for post in posts:
            if post == '.gitignore':
                continue

            final_posts.append({
                'title' : post.rpartition('-')[2],
                'link' : post.partition('-')[0]
            })

        return final_posts
    except:
        pass # do exception handling
