import os

def save(directory, id, text):
    file = open(os.path.join(directory, id), 'w')
    file.write(text)
    file.close()
