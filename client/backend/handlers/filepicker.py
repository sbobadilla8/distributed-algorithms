import os


def get_list():
    files = []
    dirs = []
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
        files.extend(filenames)
        dirs.extend(dirnames)
        break
    return {"dirs": dirs, "filenames": files}


def change(dir):
    os.chdir('./' + dir)
    return get_list()
