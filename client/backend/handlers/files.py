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


class Files:

    def __init__(self):
        self.files = []
        self.tcp_port = None
        self.managers = {}

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

    def download_file(self, file):
        download_manager = FileDownloadManager(file['filename'], file['size'], file['clients'])
        self.managers[file['filename']] = download_manager
        thread = threading.Thread(target=download_manager.initiate_download)
        thread.start()
        return ""

    def get_update(self, file):
        value = self.managers[file].get_download_progress()
        return {"value": value}
