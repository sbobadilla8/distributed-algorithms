import requests
import threading
from .filemgr import FileMgr
from .downloadmanager import FileDownloadManager

"""
file structure:
{
    filename
    size
    blocks
}
"""


def download_file(file):
    download_manager = FileDownloadManager(file['filename'], file['size'], file['clients'])
    thread = threading.Thread(target=download_manager.initiate_download)
    thread.start()
    # thread.join()
    return "", 200


class Files:

    def __init__(self):
        self.files = []
        self.tcp_port = None

    def set_port(self, port):
        self.tcp_port = port

    def get_files(self):
        return self.files

    def share_file(self, file):
        file_to_share = FileMgr(file['file'])
        r = requests.post('http://' + file['serverAddress'] + '/file', json={'filename': file_to_share.file_name,
                                                                             'port': self.tcp_port,
                                                                             "size": file_to_share.get_file_bytes_size(),
                                                                             "blocks": file_to_share.get_file_block_size(),
                                                                             "checksum": file_to_share.get_md5_hash()
                                                                             })
        self.files.append({"filename": file_to_share.file_name,
                           "size": file_to_share.get_file_bytes_size(),
                           "blocks": file_to_share.get_file_block_size()})
        return self.files

    def remove_file(self, file):
        for item in self.files:
            if item.name == file.name:
                self.files.remove(file)
        return self.files
