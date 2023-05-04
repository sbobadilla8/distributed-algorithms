# import argparse
import socket
import threading
from .filemgr import FileMgr
import pickle as rick


class FileUploadManager:
    def __init__(self, host, port):
        print("UploadManager::__init__::Starting TCP Server in ...{}:{}".format(host, port))
        self.host = host
        self.port = port
        self.fileToUpload = {}
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen()
        except OSError:
            print("TCP Server already running on port {}".format(self.port))
            return
        self.fileMgrMutex = threading.Lock()
        print("UploadManager::__init__::Listening for connections ...")
        thread = None
        while True:
            try:
                connection, address = self.socket.accept()
                print("UploadManager::__init__::Connecting to {} ...".format(address))
                thread = threading.Thread(target=self.handle_connection, args=[connection, address])
                thread.start()

            except KeyboardInterrupt:
                print("UploadManager::__init__::Keyboard interrupt")
                if thread:
                    print("UploadManager::__init__::Closing threads ...")
                    thread.join()
                break

    def handle_connection(self, connection, address):
        close_connection = False
        while not close_connection:
            message = self.read_message(connection)
            # print("UploadManager::handle_connection::Message Received: {}".format(message))
            # closeConnection = self.handle_incoming_data(connection, message)
            if message:
                action = message['action']
                if action == 'Request_Download':
                    file_name = message['payload']['file_name']
                    print("UploadManager::handle_connection::Client requests download of {}".format(file_name))
                    # Open File Manager
                    self.fileMgrMutex.acquire()
                    # print("UploadManager::handle_connection::fileToUpload = {}".format(self.fileToUpload))
                    if file_name not in self.fileToUpload.keys():
                        self.fileToUpload[file_name] = FileMgr(file_name)
                        print("UploadManager::handle_connection::{} successfully opened".format(file_name))
                    else:
                        print("UploadManager::handle_connection::{} already opened".format(file_name))
                    self.fileMgrMutex.release()
                    data_to_send = {'result': 'ACK'}
                    self.send_message(connection, data_to_send)
                if action == 'Request_Block':
                    block_index = message['payload']['block_index']
                    file_name = message['payload']['file_name']
                    # print("UploadManager::handle_connection::Client requests upload of block index: {}".format(
                    # blockIndex))
                    block_to_send = self.fileToUpload[file_name].get_block(block_index)
                    data_to_send = {'result': {'block': block_to_send}}
                    # print("UploadManager::handle_connection::Sending block {}".format(blockIndex))
                    self.send_message(connection, data_to_send)
                if action == 'Close_Connection':
                    file_name = message['payload']['file_name']
                    self.fileMgrMutex.acquire()
                    if file_name in self.fileToUpload.keys():
                        self.fileToUpload[file_name].close_file()
                        del self.fileToUpload[file_name]
                    self.fileMgrMutex.release()
                    close_connection = True
        print("UploadManager::handle_connection::Closing connection {} ...".format(address))
        connection.close()

    def send_message(self, connection, data):
        connection.send(rick.dumps(data))

    def read_message(self, connection):
        data = connection.recv(32 * 1024)
        message = rick.loads(data)
        return message

# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6000]).start()
# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6001]).start()
# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6002]).start()
# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6003]).start()
# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6004]).start()
# threading.Thread(target=FileUploadManager, args=['127.0.0.1', 6005]).start()
