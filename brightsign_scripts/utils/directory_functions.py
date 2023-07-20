import os


def shorten_filename(filename):
    filenameShort = os.path.basename(filename)  # shortens filename for convience
    return filenameShort


def create_directory(path):  # Creates new folder if doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
