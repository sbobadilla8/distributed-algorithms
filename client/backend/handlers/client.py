import socket
import time
import pickle as rick
        
class ClientConnection:
    def __init__(self, host, port):
        print("Starting Client ...")
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_message(self, data):
        msg = rick.dumps(data)
        self.socket.send(msg)

    def close(self):
        self.socket.close()

    def __del__(self):
        self.send_message('goodbye')
        print("Closing the connection ... ")
        self.close()

client = ClientConnection('127.0.0.1',5000)
time.sleep(1)
client.send_message('hello')
time.sleep(1)
client.send_message([1,2,3,4])
client.send_message({'file_name': "Image.png", 'block_id': 1, 'block': [1,2,3,4,5,6,7,8]})
time.sleep(1)
client.send_message('goodbye')