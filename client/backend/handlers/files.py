from .filemgr import FileMgr

files = []


def get_files():
    return files


def share_file(file):
    file_to_share = FileMgr(file.read())
    print(file_to_share.get_block_list())
    # files.append(file)
    return files


def remove_file(file):
    for item in files:
        if item.name == file.name:
            files.remove(file)
    return files
