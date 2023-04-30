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


def index_file(new_file, user_address):
    for file in files:
        if new_file['filename'] in file['filename']:
            file['clients'].append(user_address+":"+str(new_file['port']))
            return True
    files.append({"filename": new_file['filename'],
                  "size": new_file['size'],
                  "blocks": new_file['blocks'],
                  "clients": [user_address+":"+str(new_file['port'])],
                  "checksum": new_file['checksum']
                  })
    return True
