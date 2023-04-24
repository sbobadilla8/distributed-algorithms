files = []


def file_search(user_input):
    result = []
    for file in files:
        if user_input in file.name:
            result.append(file)
    return result


def index_file(file):
    files.append(file)
    return True
