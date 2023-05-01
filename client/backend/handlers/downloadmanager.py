import threading
import socket
import pickle as rick
import time
import random
from collections import deque
from filemgr import FileMgr
import time

class FileDownloadManager:
    def __init__(self, fileName, fileSize, peers):
        connectedPeers = []
        self.fileName = fileName
        self.fileSize = fileSize
        self.fileToDownload = None
        self.peerConnectionMutex = threading.Lock()
        self.fileWriteMutex = threading.Lock()
        self.blockIndexMutex = threading.Lock()
        
        # Create FileMgr object with given size
        fileMgrThread = threading.Thread(target=self.create_download_file)
        fileMgrThread.start()

        # Request Connection to all available peers
        # Peers which respond all get stored in connectedPeers
        print("Connecting to peers ...")
        maxThreads = 12
        connectionThreads = []
        for threadIndex in range(0, maxThreads):
            thread = threading.Thread(target=self.request_peer_connection, args=[peers[threadIndex % len(peers)], connectedPeers])
            thread.start()
            connectionThreads.append(thread)
            
        for thread in connectionThreads:
            thread.join()
        
        fileMgrThread.join()

        # Get indices of blocks to download
        self.blockIndices = deque(list( range(0, self.fileToDownload.get_file_block_size())))
        random.shuffle(self.blockIndices)

        # Request blocks from connected peers
        print("Downloading file blocks ...")
        blockThreads = []
        for threadIndex in range(0, maxThreads):
            thread = threading.Thread(target=self.request_blocks_from_peer, args=[connectedPeers[threadIndex]])
            thread.start()
            blockThreads.append(thread)

        for thread in blockThreads:
            thread.join()


        # TODO: Verify file integrity

        # Close all connected peers
        print("Closing all peers ...")
        for connectedPeer in connectedPeers:
            thread = threading.Thread(target=self.close_peer_connection, args=[connectedPeer])
            thread.start()
            thread.join()

    def create_download_file(self):
        self.fileToDownload = FileMgr(self.fileName, self.fileSize)
        
    def request_peer_connection(self, peer, connectedPeers):
        connectedPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectedPeer.settimeout(2 * 60)
        connectedPeer.connect((peer['host'], peer['port']))
        self.send_message(connectedPeer, { 'action': 'Request_Download', 'payload': { 'file_name': self.fileName}})
        message = self.read_message(connectedPeer)
        if(message['result'] == 'ACK'):
            self.peerConnectionMutex.acquire()
            try:
                connectedPeers.append(connectedPeer)
            finally:
                self.peerConnectionMutex.release()

    def request_blocks_from_peer(self, connectedPeer):
        while(True):
            # Get blockIndex from the queue in a thread safe manner
            self.blockIndexMutex.acquire()
            if(len(self.blockIndices) == 0):
                self.blockIndexMutex.release()
                break
            blockIndex = self.blockIndices.popleft()
            self.blockIndexMutex.release()
            # Request block from the connectedPeer
            # print("Requesting block {} from {}".format(blockIndex, connectedPeer.getpeername()))
            self.send_message(connectedPeer, {'action': 'Request_Block', 'payload': { 'block_index': blockIndex, 'file_name': self.fileName }})
            message = self.read_message(connectedPeer)
            if(message['result']):
                # print("Received block {} from {}".format(blockIndex, connectedPeer.getpeername()))
                block = message['result']['block']
                self.fileWriteMutex.acquire()
                self.fileToDownload.write_block(block, blockIndex)
                self.fileWriteMutex.release()
                # print("Finished writing block {} to file".format(blockIndex))

    def close_peer_connection(self, connectedPeer):
        self.send_message(connectedPeer, { 'action': 'Close_Connection', 'payload': { 'file_name': self.fileName} })
        connectedPeer.close()

    def send_message(self, connection, data):
        connection.send(rick.dumps(data))

    def read_message(self, connection):
        # self.peerConnectionMutex.acquire()
        data = connection.recv(32 * 1024)
        message = rick.loads(data)
        # self.peerConnectionMutex.release()
        return message

clients = []
clients.append({'host': '127.0.0.1', 'port': 6000})
# clients.append({'host': '127.0.0.1', 'port': 6001})
# clients.append({'host': '127.0.0.1', 'port': 6002})
# clients.append({'host': '127.0.0.1', 'port': 6003})
# clients.append({'host': '127.0.0.1', 'port': 6004})
# clients.append({'host': '127.0.0.1', 'port': 6005})
# start = time.time()
# downloadFile = FileDownloadManager("Large_File.bin", 1048576000, clients)
# downloadFile = FileDownloadManager("sql_dump.sql", 215914710, clients)
# downloadFile = FileDownloadManager("Image.png", 494787, clients)
# end = time.time()
# print("Total time required: {}seconds".format(end-start))

### Client Requests
# {
#     action: 'Request_Download' / 'Request_Block' / 'Close_Connection'
#     payload: {file_name: 'File Name'} / {block_index: 1}
# }

### Client Responses
# {
#     result: { 'ACK' / block: [1,2,3,4 . . .]}
# }