import socket
import time
        
class ClientConnection:
    def __init__(self, host, port):
        print("Starting Client ...")
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_message(self, data):
        self.socket.send(data)

client = ClientConnection('127.0.0.1',50004)
time.sleep(1)
client.send_message(b'hello')
time.sleep(3)
client.send_message(b'welcome')
time.sleep(3)
client.send_message(b'goodbye')