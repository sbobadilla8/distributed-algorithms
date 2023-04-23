files = []


def get_files():
    return files


def share_file(file):
    files.append(file)
    return files


def remove_file(file):
    for item in files:
        if item.name == file.name:
            files.remove(file)
    return files
