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
