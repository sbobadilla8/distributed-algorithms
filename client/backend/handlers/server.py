import socket
import threading

class ServerConnection:
    def __init__(self, host, port):
        print("Starting Server ...")
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        print("Listening for connections ...")
        while(True):
            self.connection, self.address = self.socket.accept()
            print("Connecting to {} ...".format(self.address))
            thread = threading.Thread(target=self.handle_connection)
            thread.start()
            #thread.join()

    def handle_connection(self):
        data = ''
        while(data != b'goodbye'):
            data = self.connection.recv(2048)
            print("Data: {}".format(data))
        #print("Closing connection ...")
        #self.connection.close()
    
    def __del__(self):
        print("Closing socket ...")
        self.socket.close()

server = ServerConnection('127.0.0.1', 50004)