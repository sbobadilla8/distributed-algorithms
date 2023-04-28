from .server import ServerConnection
from .filemgr import FileMgr

class FileShare(ServerConnection):
    def __init__(self, host, port):
        super.__init__(host, port)

    def handle_file_download(self, file_name, file_size):
        fileMgr = FileMgr(file_name, file_size)
        # Connect to other TCP clients
        # Write incoming blocks to the file
        # self.handle_incoming_data(self, fileMgr, data)

    def handle_file_upload(self, file_name):
        fileMgr = FileMgr(file_name)
        # Send requested blocks to the TCP client

    def handle_incoming_data(self, fileMgr, data):
        if(data.block):
            fileMgr.write_block(data.block)
