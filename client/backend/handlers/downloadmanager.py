import threading
import socket
import pickle as rick
import time
import random
from multiprocessing.pool import ThreadPool

class FileDownloadManager:
    def __init__(self, fileName, peers):
        connectedPeers = []
        self.mutex = threading.Lock()
        # Request Connection to all available peers
        # Peers which respond all get stored in connectedPeers
        print("Connecting to peers ...")
        for peer in peers:
            thread = threading.Thread(target=self.request_peer_connection, args=[peer, connectedPeers, fileName])
            thread.start()
            thread.join()
        print("Number of connected peers: {}".format(len(connectedPeers)))
        time.sleep(3)

        # Request blocks from connected peers
        with ThreadPool(12) as threadPool:
            results = threadPool.apply_async(func=self.request_block_from_peer, args=[connectedPeers[0], random.randint(0,4)])
            print("ThreadPool Results: {}".format(results.get()))
            results.wait()
            print("Closing ThreadPool ...")
            # threadPool.join()
            #threadPool.close()


        # Close all connected peers
        print("Closing all peers ...")
        for connectedPeer in connectedPeers:
            thread = threading.Thread(target=self.close_peer_connection, args=[connectedPeer])
            thread.start()
            thread.join()
        
    def request_peer_connection(self, peer, connectedPeers, fileName):
        peerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerConnection.settimeout(30)
        peerConnection.connect((peer['host'], peer['port']))
        self.send_message(peerConnection, { 'action': 'Request_Download', 'payload': { 'file_name': fileName}})
        message = self.read_message(peerConnection)
        if(message['result'] == 'ACK'):
            self.mutex.acquire()
            try:
                connectedPeers.append(peerConnection)
            finally:
                self.mutex.release()

    def request_block_from_peer(self, peerConnection, blockIndex):
        self.send_message(peerConnection, {'action': 'Request_Block', 'payload': { 'block_index': blockIndex }})
        message = self.read_message(peerConnection)
        print("Received Block: {}".format(message['result']))

    def close_peer_connection(self, peerConnection):
        self.send_message(peerConnection, { 'action': 'Close_Connection' })
        peerConnection.close()

    def send_message(self, connection, data):
        msg = rick.dumps(data)
        connection.send(msg)

    def read_message(self, connection):
        data = connection.recv(4096)
        msg = rick.loads(data)
        print("Received from server: {}".format(msg))
        return msg

downloadFile = FileDownloadManager("Image.png", [{'host': '127.0.0.1', 'port': 6000}])

### Client Requests
# {
#     action: 'Request_Download' / 'Request_Block' / 'Close_Connection'
#     payload: {file_name: 'File Name'} / {block_index: 1}
# }

### Client Responses
# {
#     result: { 'ACK' / block: [1,2,3,4 . . .]}
# }