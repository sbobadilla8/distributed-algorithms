import requests
from .filemgr import FileMgr

files = []
"""
file structure:
{
    filename
    size
    blocks
}
"""


def get_files():
    return files


def share_file(file):
    file_to_share = FileMgr(file)
    r = requests.post('http://localhost:8000/file', json={'filename': file_to_share.file_name,
                                                          "ip": "127.0.0.1",
                                                          "size": file_to_share.get_file_bytes_size(),
                                                          "blocks": file_to_share.get_file_block_size(),
                                                          "checksum": file_to_share.get_md5_hash()
                                                          })
    files.append({"filename": file_to_share.file_name,
                  "size": file_to_share.get_file_bytes_size(),
                  "blocks": file_to_share.get_file_block_size()})
    return files


def remove_file(file):
    for item in files:
        if item.name == file.name:
            files.remove(file)
    return files
