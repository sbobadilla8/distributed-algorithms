files = []
"""
file structure:
{
    filename
    size
    blocks
    clients
    checksum
}
"""


def file_search(user_input):
    result = []
    for file in files:
        if user_input in file['filename']:
            result.append(file)
    return result


def index_file(new_file):
    for file in files:
        if new_file['filename'] in file['filename']:
            file['clients'].append(new_file['ip'])
            return True
    files.append({"filename": new_file['filename'],
                  "size": new_file['size'],
                  "blocks": new_file['blocks'],
                  "clients": [new_file['ip']],
                  "checksum": new_file['checksum']
                  })
    return True
