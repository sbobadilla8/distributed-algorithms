# import argparse
import socket
import threading
from filemgr import FileMgr
import pickle as rick

class FileUploadManager:
    def __init__(self, host, port):
        print("Starting TCP Server ...")
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        print("Listening for connections ...")
        thread = None
        while(True):
            try:
                connection, address = self.socket.accept()
                print("Connecting to {} ...".format(address))
                thread = threading.Thread(target=self.handle_connection, args=[connection, address])
                thread.start()
                
            except KeyboardInterrupt:
                print("Keyboard interrupt")
                if(thread):
                    print("Closing threads ...")
                    thread.join()
                break

    
    def handle_connection(self, connection, address):
        closeConnection = False
        fileToUpload = None
        while(not closeConnection):
            message = self.read_message(connection)
            print("Message Received: {}".format(message))
            # closeConnection = self.handle_incoming_data(connection, message)
            if(message):
                action = message['action']
                if(action == 'Request_Download'):
                    fileName = message['payload']['file_name']
                    print("Client requests download of {}".format(fileName))
                    # Open File Manager
                    fileToUpload = FileMgr(fileName)
                    dataToSend = { 'result': 'ACK' }
                    self.send_message(connection, dataToSend)
                if(action == 'Request_Block'):
                    blockIndex = message['payload']['block_index']
                    print("Client requests upload of block index: {}".format(blockIndex))
                    blockToSend = fileToUpload.get_block(blockIndex)
                    # TODO: pickling of data is crashing when sending actual block of data
                    # dataToSend = { 'result': { 'block': blockToSend }}
                    dataToSend = { 'result': { 'block': [1,2,3,4,5] }}
                    self.send_message(connection, dataToSend)
                if(action == 'Close_Connection'):
                    closeConnection = True
        print("Closing connection {} ...".format(address))
        connection.close()

    def send_message(self, connection, message):
        data = rick.dumps(message)
        connection.send(data)

    def read_message(self, connection):
        data = connection.recv(4096)
        message = rick.loads(data)
        return message

    # def handle_incoming_data(self, connection, data):
    #     self.fileToUpload = None
    #     if(data):
    #         print(data)
    #         action = data['action']
    #         if(action == 'Request_Download'):
    #             fileName = data['payload']['file_name']
    #             print("Client requests download of {}".format(fileName))
    #             # Open File Manager
    #             #self.fileToUpload = FileMgr(fileName)
    #             dataToSend = { 'result': 'ACK' }
    #             super().send_message(connection, dataToSend)
    #         if(action == 'Request_Block'):
    #             blockIndex = data['payload']['block_index']
    #             print("Client requests upload of block index: {}".format(blockIndex))
    #             # blockToSend = self.fileToUpload.get_block(blockIndex)
    #             dataToSend = { 'result': { 'block': [1,2,3,4,5] }}
    #             super().send_message(connection, dataToSend)
    #         if(action == 'Close_Connection'):
    #             # Close File Manager
    #             return True
    #     return False

# def on_data_receive(message):
#     print("Message Received In Callback: {}".format(message))
# server = ServerConnection('127.0.0.1', 5000)

fileUploadManager = FileUploadManager('127.0.0.1', 6000)