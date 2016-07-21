import os

def save(directory, id, text):
    try:
        file = open(os.path.join(directory, id), 'w')
        file.write(text)
        file.close()
        return False
    except:
        return True
