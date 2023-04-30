# import argparse
import socket
import threading
import pickle as rick

class ServerConnection:
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
        msg = ''
        while(msg != 'goodbye'):
            data = connection.recv(4096)
            msg = rick.loads(data)
            print("Message Received: {}".format(msg))
            # self.handle_incoming_data(msg)
        print("Closing connection {} ...".format(address))
        connection.close()

    def handle_incoming_data(self, data):
        # FileMgr.write_block_static_function(msg)
        print("Data Received: {}".format(data))

# def on_data_receive(msg):
#     print("Message Received In Callback: {}".format(msg))
# server = ServerConnection('127.0.0.1', 5000)